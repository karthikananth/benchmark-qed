#!/usr/bin/env python3
"""
LGR Search V5 — Full 100-question search with short_id resolution.

Sends questions to LGR via V2 queue/blob protocol, resolves chunk short_ids
via parquet lookup, saves answers + retrieval data to NFS with per-question
checkpointing.

Environment Variables:
    AZURE_CLIENT_ID: Managed identity client ID
    LGR_STORAGE_ACCOUNT: Storage account for LGR queues/blobs
    LGR_IN_QUEUE: Input queue name
    LGR_BLOB_CONTAINER: Blob container for responses
    LGR_KB_NAME: Knowledge base name (function_name in payload)
    CHECKPOINT_DIR: NFS checkpoint directory
    LGR_POLL_INTERVAL: Seconds between blob polls (default: 10)
    LGR_TIMEOUT: Timeout per question in seconds (default: 600)
"""

import base64
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import ContainerClient
from azure.storage.queue import QueueClient

# Configuration from environment
MI_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID", "5d6ec60b-bc36-4e8c-88f6-a9667816db88")
STORAGE_ACCOUNT = os.environ.get("LGR_STORAGE_ACCOUNT", "stdbksf75kdp9aaaa")
IN_QUEUE = os.environ.get("LGR_IN_QUEUE", "bkshlfleukemialgr-bkshlfleukemiaeval-1-in")
BLOB_CONTAINER = os.environ.get("LGR_BLOB_CONTAINER", "toolcall-results")
KB_NAME = os.environ.get("LGR_KB_NAME", "bkshlfleukemiaeval")
CHECKPOINT_DIR = Path(os.environ.get("CHECKPOINT_DIR", "/mnt/checkpoints/benchmark-qed-leukemia-v5"))
POLL_INTERVAL = int(os.environ.get("LGR_POLL_INTERVAL", "10"))
TIMEOUT = int(os.environ.get("LGR_TIMEOUT", "600"))

OUTPUT_DIR = CHECKPOINT_DIR / "output"
SEARCH_CHECKPOINT_DIR = OUTPUT_DIR / "lgr_search_checkpoints"
ANSWERS_FILE = OUTPUT_DIR / "answers.json"
RETRIEVAL_FILE = OUTPUT_DIR / "lgr_retrieval_data.json"
TEXT_UNITS_PARQUET = OUTPUT_DIR / "text_units.parquet"


def log(msg: str) -> None:
    """Print with timestamp and flush."""
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def log_section(title: str) -> None:
    """Print section header."""
    print(f"\n{'='*60}", flush=True)
    print(f"  {title}", flush=True)
    print(f"{'='*60}", flush=True)


def build_text_to_shortid_lookup(parquet_path: Path) -> dict[str, str]:
    """Build text prefix → short_id lookup from parquet."""
    log(f"Loading text_units from {parquet_path}...")
    df = pd.read_parquet(parquet_path, columns=["text", "short_id"])
    lookup = {}
    for _, row in df.iterrows():
        key = row["text"][:200]
        lookup[key] = str(row["short_id"])
    log(f"Built lookup: {len(lookup)} entries")
    return lookup


def load_questions(output_dir: Path) -> list[dict]:
    """Load and combine all selected questions from AutoQ output."""
    question_types = ["data_global", "data_local", "data_linked"]
    all_questions = []

    for qtype in question_types:
        selected = output_dir / f"{qtype}_questions" / "selected_questions.json"
        if selected.exists():
            with open(selected) as f:
                questions = json.load(f)
            if isinstance(questions, list):
                for q in questions:
                    q["_source_type"] = qtype
                all_questions.extend(questions)
                log(f"  {qtype}: {len(questions)} questions")

    log(f"Total: {len(all_questions)} questions")
    return all_questions


def load_checkpoints(checkpoint_dir: Path) -> dict[str, dict]:
    """Load completed question checkpoints."""
    completed = {}
    if not checkpoint_dir.exists():
        return completed

    for fname in checkpoint_dir.iterdir():
        if fname.suffix == ".json":
            try:
                with open(fname) as f:
                    data = json.load(f)
                if data.get("status") == "success":
                    completed[data["question_id"]] = data
            except Exception:
                pass

    return completed


def send_v2_question(
    in_queue: QueueClient, question_id: str, question_text: str, kb_name: str
) -> str:
    """Send V2 format question to LGR IN queue. Returns toolCallId."""
    tool_call_id = f"tc_{question_id.replace('-', '')[:20]}"
    payload = {
        "function_name": kb_name,
        "correlationId": question_id,
        "toolCallId": tool_call_id,
        "discoveryResponseId": f"/projects/benchmark-qed/conversations/eval/responses/{question_id}",
        "agentName": "KbAgent",
        "function_args": {"query": question_text, "searchType": 0},
    }
    encoded = base64.b64encode(json.dumps(payload).encode()).decode()
    in_queue.send_message(encoded)
    return tool_call_id


def poll_blob_response(
    blob_container: ContainerClient,
    correlation_id: str,
    tool_call_id: str,
    timeout: int,
    poll_interval: int,
) -> dict | None:
    """Poll blob storage for V2 response."""
    blob_path = f"{correlation_id}/{tool_call_id}/result.json"
    start = time.time()

    while time.time() - start < timeout:
        try:
            blob_client = blob_container.get_blob_client(blob_path)
            data = blob_client.download_blob().readall()
            result = json.loads(data.decode("utf-8"))
            blob_client.delete_blob()
            return {
                "text": result.get("text", ""),
                "annotations": result.get("annotations", []),
                "latency": time.time() - start,
            }
        except Exception as e:
            if "BlobNotFound" in str(e) or "ResourceNotFound" in str(
                type(e).__name__
            ):
                elapsed = int(time.time() - start)
                if elapsed % 30 == 0 and elapsed > 0:
                    log(f"    Still polling... {elapsed}s")
                time.sleep(poll_interval)
            else:
                log(f"    ERROR polling: {e}")
                raise

    return None


def resolve_chunks(
    annotations: list, text_to_id: dict[str, str]
) -> tuple[list[dict], int, int]:
    """Extract and resolve chunks from LGR annotations.

    Returns: (resolved_chunks, resolved_count, missing_count)
    """
    chunks = []
    resolved = 0
    missing = 0

    for ann in annotations:
        file_id = ann.get("file_id", "")
        for chunk_text in ann.get("text_chunks", []):
            key = chunk_text[:200]
            short_id = text_to_id.get(key)
            if short_id:
                chunks.append({
                    "chunk_id": short_id,
                    "short_id": short_id,
                    "text": chunk_text,
                    "file_id": file_id,
                })
                resolved += 1
            else:
                chunks.append({
                    "chunk_id": f"unresolved_{missing}",
                    "short_id": None,
                    "text": chunk_text,
                    "file_id": file_id,
                })
                missing += 1

    return chunks, resolved, missing


def save_checkpoint(
    checkpoint_dir: Path, question_id: str, data: dict
) -> None:
    """Save per-question checkpoint."""
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_file = checkpoint_dir / f"{question_id}.json"
    with open(checkpoint_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_combined_outputs(
    checkpoints: dict[str, dict],
    answers_file: Path,
    retrieval_file: Path,
) -> None:
    """Save combined answers.json and lgr_retrieval_data.json from checkpoints."""
    answers = []
    retrieval = []

    for qid, cp in checkpoints.items():
        answers.append({
            "question_id": cp["question_id"],
            "question": cp["question_text"],
            "answer": cp["answer"],
            "latency_seconds": cp.get("latency"),
            "status": cp.get("status", "success"),
        })
        retrieval.append({
            "question_id": cp["question_id"],
            "text": cp["question_text"],
            "context": cp.get("context", []),
        })

    with open(answers_file, "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=2, ensure_ascii=False)

    with open(retrieval_file, "w", encoding="utf-8") as f:
        json.dump(retrieval, f, indent=2, ensure_ascii=False)


def main() -> None:
    log_section("LGR Search V5 — Starting")
    log(f"Storage: {STORAGE_ACCOUNT}")
    log(f"Queue: {IN_QUEUE}")
    log(f"KB: {KB_NAME}")
    log(f"Checkpoint: {CHECKPOINT_DIR}")
    log(f"Poll interval: {POLL_INTERVAL}s, Timeout: {TIMEOUT}s")

    # Step 1: Build short_id lookup
    log_section("Step 1: Building short_id lookup from parquet")
    text_to_id = build_text_to_shortid_lookup(TEXT_UNITS_PARQUET)

    # Step 2: Load questions
    log_section("Step 2: Loading questions")
    questions = load_questions(OUTPUT_DIR)
    if not questions:
        log("ERROR: No questions found!")
        sys.exit(1)

    # Step 3: Load existing checkpoints
    log_section("Step 3: Loading checkpoints")
    completed = load_checkpoints(SEARCH_CHECKPOINT_DIR)
    if completed:
        log(f"Resuming: {len(completed)}/{len(questions)} already completed")
    else:
        log("Starting fresh — no checkpoints found")

    # Step 4: Initialize Azure clients
    log_section("Step 4: Connecting to Azure")
    cred = ManagedIdentityCredential(client_id=MI_CLIENT_ID)
    queue_url = f"https://{STORAGE_ACCOUNT}.queue.core.windows.net"
    in_queue = QueueClient(queue_url, IN_QUEUE, credential=cred)
    blob_client = ContainerClient(
        f"https://{STORAGE_ACCOUNT}.blob.core.windows.net",
        BLOB_CONTAINER,
        credential=cred,
    )
    log("Connected to queue and blob storage")

    # Step 5: Process questions
    log_section("Step 5: Processing questions")
    total = len(questions)
    stats = {"success": len(completed), "timeout": 0, "error": 0}
    total_resolved = 0
    total_missing = 0
    total_chunks = 0

    for i, q in enumerate(questions, 1):
        q_id = q.get("question_id", q.get("id", f"q_{i}"))
        q_text = q.get("question_text", q.get("question", q.get("text", "")))
        q_type = q.get("_source_type", "unknown")

        # Skip if already completed
        if q_id in completed:
            cp = completed[q_id]
            ctx = cp.get("context", [])
            log(f"[{i}/{total}] SKIP (checkpointed) {q_id[:12]}... | {len(ctx)} chunks")
            continue

        log(f"\n[{i}/{total}] {'─'*50}")
        log(f"  ID:   {q_id}")
        log(f"  Type: {q_type}")
        log(f"  Q:    {q_text[:120]}...")

        # Send to LGR
        try:
            tool_call_id = send_v2_question(in_queue, q_id, q_text, KB_NAME)
            log(f"  Sent to queue → polling blob {q_id[:8]}/{tool_call_id}...")
        except Exception as e:
            log(f"  ERROR sending: {e}")
            stats["error"] += 1
            continue

        # Poll for response
        result = poll_blob_response(
            blob_client, q_id, tool_call_id, TIMEOUT, POLL_INTERVAL
        )

        if result:
            # Resolve chunks
            chunks, resolved, missing = resolve_chunks(
                result["annotations"], text_to_id
            )
            total_resolved += resolved
            total_missing += missing
            total_chunks += len(chunks)

            log(f"  ✓ Response: {len(result['text'])} chars in {result['latency']:.0f}s")
            log(f"  ✓ Chunks: {len(chunks)} total, {resolved} resolved, {missing} unresolved")

            # Log each chunk's short_id
            for j, chunk in enumerate(chunks):
                sid = chunk.get("short_id", "NONE")
                log(f"    chunk[{j}]: short_id={sid}, file_id={chunk.get('file_id','')}, text={chunk['text'][:60]}...")

            # Save checkpoint
            checkpoint = {
                "question_id": q_id,
                "question_text": q_text,
                "question_type": q_type,
                "answer": result["text"],
                "context": [
                    {"chunk_id": c["chunk_id"], "short_id": c["short_id"], "text": c["text"]}
                    for c in chunks
                ],
                "annotations": result["annotations"],
                "latency": result["latency"],
                "chunks_resolved": resolved,
                "chunks_missing": missing,
                "status": "success",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            save_checkpoint(SEARCH_CHECKPOINT_DIR, q_id, checkpoint)
            completed[q_id] = checkpoint
            stats["success"] += 1
            log(f"  ✓ Checkpointed to NFS")

        else:
            log(f"  ✗ TIMEOUT after {TIMEOUT}s")
            checkpoint = {
                "question_id": q_id,
                "question_text": q_text,
                "question_type": q_type,
                "answer": "[TIMEOUT]",
                "context": [],
                "latency": TIMEOUT,
                "chunks_resolved": 0,
                "chunks_missing": 0,
                "status": "timeout",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            save_checkpoint(SEARCH_CHECKPOINT_DIR, q_id, checkpoint)
            completed[q_id] = checkpoint
            stats["timeout"] += 1

        # Save combined outputs after each question (incremental)
        save_combined_outputs(completed, ANSWERS_FILE, RETRIEVAL_FILE)

        # Brief delay between questions
        if i < total:
            time.sleep(2)

    # Final summary
    log_section("LGR Search Complete")
    log(f"Total questions: {total}")
    log(f"Success: {stats['success']}")
    log(f"Timeout: {stats['timeout']}")
    log(f"Error: {stats['error']}")
    log(f"Total chunks: {total_chunks}")
    log(f"Chunks resolved: {total_resolved} ({total_resolved*100//max(total_chunks,1)}%)")
    log(f"Chunks unresolved: {total_missing}")
    log(f"Answers: {ANSWERS_FILE}")
    log(f"Retrieval data: {RETRIEVAL_FILE}")
    log(f"Checkpoints: {SEARCH_CHECKPOINT_DIR}")


if __name__ == "__main__":
    main()
