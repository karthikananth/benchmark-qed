"""LLM Topic Classification using keyword-guided document samples.

Sends sampled text for each document to GPT-5-mini, scores 0-5 per topic.
Uses async concurrency with checkpointing.

Input: document_samples.json, doc_id_to_filename.json
Output: llm_topic_scores.json
"""
import asyncio
import json
import os
import time
from tqdm import tqdm
from openai import AsyncAzureOpenAI
from azure.identity import AzureCliCredential, get_bearer_token_provider

ENDPOINT = "https://aoai-lgr-poc.openai.azure.com/"
DEPLOYMENT = "gpt-5.2"
API_VERSION = "2024-12-01-preview"

CONCURRENCY = 30
CHECKPOINT_EVERY = 10
CHECKPOINT_FILE = "llm_topic_checkpoints/progress.json"
OUTPUT_FILE = "llm_topic_scores.json"

SYSTEM_PROMPT = """Score this scientific document's relevance to each of the following 7 topics on a scale of 0-5:

0 = Not mentioned at all
1 = Tangential mention (a few words, not a focus)
2 = Brief discussion (a paragraph or two, minor topic)
3 = Substantive discussion (a full section or repeated throughout)
4 = Major focus (one of the paper's main themes)
5 = Primary subject (the paper is fundamentally about this topic)

Topics and their defining concepts:
1. Disease — leukemia, AML (acute myeloid leukemia), hematology, metastases
2. Differentiation — cell differentiation therapy, ATRA (all-trans retinoic acid)
3. Cardiac_safety — hERG channel, QT prolongation, arrhythmia, cardiotoxicity
4. Solubility — aqueous solubility, bioavailability, logP, logD
5. Permeability — cell membrane permeability, PAMPA assay, Caco-2, MDCK
6. Metabolic_stability — CYP450 enzymes, half-life, clearance, CLint, microsomes, hepatocytes
7. Drug_discovery — medicinal chemistry, SAR (structure-activity relationships), lead optimization, lead generation, structure-based drug design, Lipinski rules, pharmacophore, IC50, EC50

Respond with ONLY a JSON object (no markdown, no explanation):
{"Disease": N, "Differentiation": N, "Cardiac_safety": N, "Solubility": N, "Permeability": N, "Metabolic_stability": N, "Drug_discovery": N}"""

TOPICS = ["Disease", "Differentiation", "Cardiac_safety", "Solubility",
          "Permeability", "Metabolic_stability", "Drug_discovery"]


def load_checkpoint() -> dict:
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {"scores": {}, "errors": {}}


def save_checkpoint(data: dict):
    os.makedirs(os.path.dirname(CHECKPOINT_FILE), exist_ok=True)
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(data, f)


def validate_scores(result: dict) -> bool:
    for topic in TOPICS:
        if topic not in result:
            return False
        if not isinstance(result[topic], (int, float)):
            return False
        if result[topic] < 0 or result[topic] > 5:
            return False
    return True


async def score_document(client, semaphore, doc_id, sampled_text, results, errors, counter, pbar):
    async with semaphore:
        for attempt in range(3):
            try:
                response = await client.chat.completions.create(
                    model=DEPLOYMENT,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Classify this document:\n\n<document>\n{sampled_text}\n</document>"}
                    ],
                    temperature=0,
                    max_completion_tokens=200,
                    response_format={"type": "json_object"},
                )
                text = response.choices[0].message.content
                if not text:
                    if attempt == 2:
                        errors[doc_id] = "empty_response"
                        counter["errors"] += 1
                        pbar.update(1)
                    continue
                # Try to extract JSON from response (may have markdown wrapping)
                if "{" in text:
                    json_str = text[text.index("{"):text.rindex("}") + 1]
                else:
                    json_str = text
                scores = json.loads(json_str)
                if validate_scores(scores):
                    # Convert floats to ints
                    results[doc_id] = {t: int(scores[t]) for t in TOPICS}
                    counter["done"] += 1
                    counter["input_tokens"] += response.usage.prompt_tokens
                    counter["output_tokens"] += response.usage.completion_tokens
                    pbar.update(1)
                    return
                else:
                    if attempt == 2:
                        errors[doc_id] = f"invalid_scores: {text[:200]}"
                        counter["errors"] += 1
            except Exception as e:
                if attempt == 2:
                    errors[doc_id] = str(e)[:200]
                    counter["errors"] += 1
                    pbar.update(1)
                    if counter["errors"] <= 5:
                        print(f"  ERROR [{counter['errors']}]: {str(e)[:150]}")
                else:
                    wait = (2 ** attempt) * 2
                    await asyncio.sleep(wait)


async def main():
    # Load inputs
    print("Loading document samples...")
    with open("document_samples.json") as f:
        samples = json.load(f)
    print(f"Loaded {len(samples)} document samples")

    with open("doc_id_to_filename.json") as f:
        filenames = json.load(f)

    # Load checkpoint
    checkpoint = load_checkpoint()
    already_done = set(checkpoint["scores"].keys())
    print(f"Checkpoint: {len(already_done)} already scored")

    # Filter to remaining docs
    remaining = {k: v for k, v in samples.items() if k not in already_done}
    print(f"Remaining: {len(remaining)} documents")

    if not remaining:
        print("All documents already scored!")
        return

    # Create client with Entra ID auth
    token_provider = get_bearer_token_provider(
        AzureCliCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = AsyncAzureOpenAI(
        azure_endpoint=ENDPOINT,
        azure_ad_token_provider=token_provider,
        api_version=API_VERSION,
    )

    semaphore = asyncio.Semaphore(CONCURRENCY)
    results = dict(checkpoint["scores"])
    errors = dict(checkpoint.get("errors", {}))
    counter = {"done": len(already_done), "errors": 0, "input_tokens": 0, "output_tokens": 0}
    start_time = time.time()

    # Process all with tqdm progress bar
    doc_ids = list(remaining.keys())
    pbar = tqdm(total=len(doc_ids), desc="Scoring", unit="doc",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] Errors:{postfix}")
    pbar.set_postfix_str("0")

    batch_start = 0
    while batch_start < len(doc_ids):
        batch_end = min(batch_start + CHECKPOINT_EVERY, len(doc_ids))
        batch = doc_ids[batch_start:batch_end]

        tasks = [
            score_document(client, semaphore, doc_id, remaining[doc_id]["sampled_text"], results, errors, counter, pbar)
            for doc_id in batch
        ]
        await asyncio.gather(*tasks)

        # Checkpoint
        checkpoint["scores"] = results
        checkpoint["errors"] = errors
        save_checkpoint(checkpoint)
        pbar.set_postfix_str(str(counter["errors"]))

        batch_start = batch_end

    pbar.close()
    await client.close()

    # Save final output with filenames
    elapsed = time.time() - start_time
    output = {
        "metadata": {
            "model": DEPLOYMENT,
            "endpoint": ENDPOINT,
            "documents_scored": len(results),
            "errors": len(errors),
            "input_tokens": counter["input_tokens"],
            "output_tokens": counter["output_tokens"],
            "duration_seconds": round(elapsed, 1),
            "sampling_method": "keyword-guided (first2 + top3-hits + last1)",
        },
        "scores": {}
    }

    for doc_id, scores in results.items():
        fn_info = filenames.get(doc_id, {})
        output["scores"][doc_id] = {
            **scores,
            "filename": fn_info.get("filename", "unknown"),
        }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n{'='*60}")
    print(f"COMPLETE: {len(results)} docs scored in {elapsed:.0f}s")
    print(f"Errors: {len(errors)}")
    print(f"Tokens: {counter['input_tokens']:,} in / {counter['output_tokens']:,} out")
    input_cost = counter["input_tokens"] / 1e6 * 0.15
    output_cost = counter["output_tokens"] / 1e6 * 0.60
    print(f"Cost: ${input_cost + output_cost:.2f}")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
