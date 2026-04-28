#!/usr/bin/env python3
"""
GRZ Search + AutoE Pipeline — Send 100 questions to GRZ, save answers for assertion scoring.

GRZ uses REST API (POST /search → poll GET /search/{job_id}).
Saves answers in same format as LGR for direct AutoE comparison.

Environment Variables:
    GRZ_ENDPOINT: GRZ search endpoint URL
    CHECKPOINT_DIR: NFS checkpoint directory
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


GRZ_ENDPOINT = os.environ.get(
    "GRZ_ENDPOINT",
    "https://grz-search.purplesky-56dbb610.swedencentral.azurecontainerapps.io"
)
CHECKPOINT_DIR = Path(os.environ.get("CHECKPOINT_DIR", "/mnt/checkpoints/benchmark-qed-leukemia-v5"))
OUTPUT_DIR = CHECKPOINT_DIR / "output"
GRZ_CHECKPOINT_DIR = OUTPUT_DIR / "grz_search_checkpoints"
GRZ_ANSWERS_FILE = OUTPUT_DIR / "grz_answers.json"
POLL_INTERVAL = 10
TIMEOUT = 600


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def log_section(title: str) -> None:
    print(f"\n{'='*60}", flush=True)
    print(f"  {title}", flush=True)
    print(f"{'='*60}", flush=True)


def load_questions(output_dir: Path) -> list[dict]:
    """Load combined questions from AutoQ output."""
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
    """Load completed GRZ search checkpoints."""
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


def search_grz(query: str) -> dict | None:
    """Send query to GRZ and poll for response."""
    # POST to start search
    try:
        resp = requests.post(
            f"{GRZ_ENDPOINT}/search",
            json={"query": query},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        log(f"    ERROR posting: {e}")
        return None

    job_id = data.get("job_id")
    status = data.get("status")

    # If already complete (synchronous response)
    if status == "complete":
        return data

    # Poll for completion
    t0 = time.time()
    while time.time() - t0 < TIMEOUT:
        try:
            poll = requests.get(
                f"{GRZ_ENDPOINT}/search/{job_id}",
                timeout=30,
            )
            poll.raise_for_status()
            result = poll.json()
            if result.get("status") == "complete":
                return result
            elapsed = int(time.time() - t0)
            if elapsed % 30 == 0 and elapsed > 0:
                log(f"    Still polling... {elapsed}s")
            time.sleep(POLL_INTERVAL)
        except Exception as e:
            log(f"    Poll error: {e}")
            time.sleep(POLL_INTERVAL)

    return None


def save_checkpoint(checkpoint_dir: Path, question_id: str, data: dict) -> None:
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    with open(checkpoint_dir / f"{question_id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_answers(completed: dict[str, dict], output_file: Path) -> None:
    answers = []
    for qid, cp in completed.items():
        answers.append({
            "question_id": cp["question_id"],
            "question": cp["question_text"],
            "answer": cp["answer"],
            "latency_seconds": cp.get("latency"),
            "status": cp.get("status", "success"),
        })
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=2, ensure_ascii=False)


def main() -> None:
    log_section("GRZ Search — Starting")
    log(f"Endpoint: {GRZ_ENDPOINT}")
    log(f"Checkpoint: {CHECKPOINT_DIR}")

    # Step 1: Load questions
    log_section("Step 1: Loading questions")
    questions = load_questions(OUTPUT_DIR)
    if not questions:
        log("ERROR: No questions found!")
        sys.exit(1)

    # Step 2: Load checkpoints
    log_section("Step 2: Loading checkpoints")
    completed = load_checkpoints(GRZ_CHECKPOINT_DIR)
    if completed:
        log(f"Resuming: {len(completed)}/{len(questions)} already completed")
    else:
        log("Starting fresh")

    # Step 3: Verify GRZ endpoint is reachable
    log_section("Step 3: Checking GRZ endpoint")
    try:
        health = requests.get(f"{GRZ_ENDPOINT}/health", timeout=10)
        log(f"Health check: {health.status_code}")
    except Exception:
        log("Health endpoint not available, proceeding anyway")

    # Step 4: Process questions
    log_section("Step 4: Processing questions")
    total = len(questions)
    stats = {"success": len(completed), "timeout": 0, "error": 0}

    for i, q in enumerate(questions, 1):
        q_id = q.get("question_id", q.get("id", f"q_{i}"))
        q_text = q.get("question_text", q.get("question", q.get("text", "")))
        q_type = q.get("_source_type", "unknown")

        if q_id in completed:
            log(f"[{i}/{total}] SKIP (checkpointed) {q_id[:12]}...")
            continue

        log(f"\n[{i}/{total}] {'─'*50}")
        log(f"  ID:   {q_id}")
        log(f"  Type: {q_type}")
        log(f"  Q:    {q_text[:120]}...")

        t0 = time.time()
        result = search_grz(q_text)
        latency = time.time() - t0

        if result and result.get("status") == "complete":
            answer = result.get("response", "")
            sources = result.get("sources", [])
            total_chunks = sum(len(s.get("cited_chunk_ids", [])) for s in sources)

            log(f"  ✓ Response: {len(answer)} chars in {latency:.0f}s")
            log(f"  ✓ Sources: {len(sources)} documents, {total_chunks} cited chunks")

            checkpoint = {
                "question_id": q_id,
                "question_text": q_text,
                "question_type": q_type,
                "answer": answer,
                "sources": sources,
                "sampled_chunks": result.get("sampled_chunks"),
                "latency": latency,
                "retrieve_seconds": result.get("retrieve_seconds"),
                "answer_seconds": result.get("answer_seconds"),
                "status": "success",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            save_checkpoint(GRZ_CHECKPOINT_DIR, q_id, checkpoint)
            completed[q_id] = checkpoint
            stats["success"] += 1
            log(f"  ✓ Checkpointed")
        else:
            log(f"  ✗ TIMEOUT/ERROR after {latency:.0f}s")
            checkpoint = {
                "question_id": q_id,
                "question_text": q_text,
                "question_type": q_type,
                "answer": "[TIMEOUT]",
                "sources": [],
                "latency": latency,
                "status": "timeout",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            save_checkpoint(GRZ_CHECKPOINT_DIR, q_id, checkpoint)
            completed[q_id] = checkpoint
            stats["timeout"] += 1

        # Save incrementally
        save_answers(completed, GRZ_ANSWERS_FILE)

        if i < total:
            time.sleep(2)

    # Summary
    log_section("GRZ Search Complete")
    log(f"Total: {total}")
    log(f"Success: {stats['success']}")
    log(f"Timeout: {stats['timeout']}")
    log(f"Error: {stats['error']}")
    log(f"Answers: {GRZ_ANSWERS_FILE}")


if __name__ == "__main__":
    main()
