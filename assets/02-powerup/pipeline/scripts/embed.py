"""
Stage 4-5: Embedding + Upsert to Supabase
==========================================
Reads chunked output, embeds each chunk via OpenAI, and upserts
the results into the Supabase chunks table.

Usage:
    python embed.py --input ./output/chunked.json

Prerequisites:
    - OPENAI_API_KEY environment variable
    - SUPABASE_URL and SUPABASE_KEY environment variables
    - pip install openai supabase
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import openai
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536
BATCH_SIZE = 100  # OpenAI allows up to 2048, but 100 is safer
MAX_RETRIES = 5
INITIAL_BACKOFF = 1.0  # seconds
UPSERT_BATCH_SIZE = 100


def get_supabase_client():
    """Create Supabase client from environment variables."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("Error: Set SUPABASE_URL and SUPABASE_KEY environment variables.")
        sys.exit(1)
    return create_client(url, key)


def get_openai_client():
    """Create OpenAI client from environment variable."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: Set OPENAI_API_KEY environment variable.")
        sys.exit(1)
    return openai.OpenAI(api_key=api_key)


# ---------------------------------------------------------------------------
# Stage 4: Embedding
# ---------------------------------------------------------------------------
def embed_batch(client, texts: list[str]) -> tuple[list[list[float]], int]:
    """
    Embed a batch of texts. Returns (embeddings, total_tokens).
    Includes retry logic with exponential backoff for rate limits.
    """
    backoff = INITIAL_BACKOFF

    for attempt in range(MAX_RETRIES):
        try:
            response = client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=texts,
            )
            embeddings = [item.embedding for item in response.data]
            total_tokens = response.usage.total_tokens
            return embeddings, total_tokens
        except openai.RateLimitError:
            if attempt < MAX_RETRIES - 1:
                print(f"    Rate limited. Waiting {backoff:.1f}s...")
                time.sleep(backoff)
                backoff *= 2
            else:
                raise
        except openai.APIError as e:
            if attempt < MAX_RETRIES - 1:
                print(f"    API error: {e}. Retrying in {backoff:.1f}s...")
                time.sleep(backoff)
                backoff *= 2
            else:
                raise

    return [], 0  # Should not reach here


def embed_all_chunks(client, chunked_files: list[dict]) -> tuple[list[dict], int]:
    """
    Embed all chunks across all files. Returns updated file data
    with embeddings attached, plus total token usage.
    """
    total_tokens = 0

    for file_data in chunked_files:
        chunks = file_data["chunks"]
        texts = [c["content"] for c in chunks]

        # Process in batches
        all_embeddings = []
        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i : i + BATCH_SIZE]
            embeddings, tokens = embed_batch(client, batch)
            all_embeddings.extend(embeddings)
            total_tokens += tokens

        # Attach embeddings to chunks
        for chunk, embedding in zip(chunks, all_embeddings):
            chunk["embedding"] = embedding

    return chunked_files, total_tokens


# ---------------------------------------------------------------------------
# Stage 5: Upsert to Supabase
# ---------------------------------------------------------------------------
def upsert_file_chunks(supabase, file_data: dict) -> int:
    """
    Delete old chunks (if re-processing) and insert new ones.
    Returns the number of chunks inserted.
    """
    file_id = file_data["file_metadata_id"]
    chunks = file_data["chunks"]

    # Step 1: Delete old chunks for this file
    supabase.table("chunks").delete().eq("file_id", file_id).execute()

    # Step 2: Batch insert new chunks
    inserted = 0
    for i in range(0, len(chunks), UPSERT_BATCH_SIZE):
        batch = chunks[i : i + UPSERT_BATCH_SIZE]
        rows = []
        for chunk in batch:
            rows.append({
                "file_id": file_id,
                "chunk_index": chunk["chunk_index"],
                "content": chunk["content"],
                "embedding": chunk["embedding"],
                "token_count": chunk["token_count"],
                "chunk_metadata": json.dumps({
                    "section_heading": chunk.get("section_heading"),
                    "hierarchy_level": chunk.get("hierarchy_level", 0),
                    "has_table": chunk.get("has_table", False),
                }),
            })
        supabase.table("chunks").insert(rows).execute()
        inserted += len(rows)

    # Step 3: Update file_metadata
    supabase.table("file_metadata").update({
        "status": "completed",
        "chunk_count": inserted,
        "chunk_strategy": file_data["chunk_strategy"],
        "embedding_model": EMBEDDING_MODEL,
    }).eq("id", file_id).execute()

    return inserted


def mark_failed(supabase, file_id: str, error: str):
    """Mark a file as failed in file_metadata."""
    supabase.table("file_metadata").update({
        "status": "failed",
        "error_message": error[:500],  # Truncate long errors
    }).eq("id", file_id).execute()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="RAG Pipeline — Embed & Upsert")
    parser.add_argument(
        "--input",
        default="./output/chunked.json",
        help="Path to chunked.json from chunking step",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Embed only — don't upsert to Supabase",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        print("Run chunking.py first.")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        chunked_files = json.load(f)

    total_chunks = sum(len(f["chunks"]) for f in chunked_files)

    # --- Stage 4: Embedding ---
    print("=" * 60)
    print("Stage 4: Embedding")
    print("=" * 60)
    print(f"\nEmbedding {total_chunks} chunks across {len(chunked_files)} files...")
    print(f"Model: {EMBEDDING_MODEL} ({EMBEDDING_DIMENSIONS} dimensions)")
    print(f"Batch size: {BATCH_SIZE}\n")

    openai_client = get_openai_client()

    for file_data in chunked_files:
        file_name = file_data["file_name"]
        n_chunks = len(file_data["chunks"])
        print(f"  {file_name}: {n_chunks} chunks...", end=" ")

        texts = [c["content"] for c in file_data["chunks"]]
        all_embeddings = []
        file_tokens = 0

        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i : i + BATCH_SIZE]
            embeddings, tokens = embed_batch(openai_client, batch)
            all_embeddings.extend(embeddings)
            file_tokens += tokens

        for chunk, embedding in zip(file_data["chunks"], all_embeddings):
            chunk["embedding"] = embedding

        print(f"OK ({file_tokens} tokens)")

    if args.dry_run:
        print("\n[Dry run] Skipping Supabase upsert.")

        # Write embedded output for inspection
        output_path = input_path.parent / "embedded.json"
        # Strip embeddings for readable output (they're huge)
        preview = []
        for f in chunked_files:
            preview.append({
                "file_name": f["file_name"],
                "chunk_count": len(f["chunks"]),
                "sample_embedding_length": (
                    len(f["chunks"][0]["embedding"]) if f["chunks"] else 0
                ),
            })
        with open(output_path, "w") as fout:
            json.dump(preview, fout, indent=2)
        print(f"Preview saved to: {output_path}")
        return

    # --- Stage 5: Upsert ---
    print(f"\n{'=' * 60}")
    print("Stage 5: Upsert to Supabase")
    print("=" * 60)

    supabase = get_supabase_client()
    total_inserted = 0
    failures = 0

    for file_data in chunked_files:
        file_name = file_data["file_name"]
        print(f"\n  Upserting: {file_name}...", end=" ")
        try:
            count = upsert_file_chunks(supabase, file_data)
            total_inserted += count
            print(f"OK ({count} chunks)")
        except Exception as e:
            failures += 1
            print(f"FAILED: {e}")
            mark_failed(supabase, file_data["file_metadata_id"], str(e))

    # --- Summary ---
    print(f"\n{'=' * 60}")
    print("Pipeline Complete")
    print("=" * 60)
    print(f"  Files processed: {len(chunked_files)}")
    print(f"  Chunks inserted: {total_inserted}")
    print(f"  Failures:        {failures}")

    if failures == 0:
        print("\nVerification queries:")
        print("  SELECT status, count(*) FROM file_metadata GROUP BY status;")
        print("  SELECT f.file_name, f.chunk_count")
        print("    FROM file_metadata f WHERE f.status = 'completed';")
    else:
        print(f"\n{failures} file(s) failed. Check file_metadata for error details:")
        print("  SELECT file_name, error_message FROM file_metadata WHERE status = 'failed';")


if __name__ == "__main__":
    main()
