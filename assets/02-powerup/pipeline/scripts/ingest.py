"""
Stage 1: File Intake
====================
Scans the source folder, registers files in Supabase file_metadata,
and outputs a JSON manifest of files ready for conversion.

Usage:
    python ingest.py --source-dir ../source-files --output-dir ./output

Prerequisites:
    - SUPABASE_URL and SUPABASE_KEY environment variables
    - pip install supabase
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SUPPORTED_EXTENSIONS = {".md", ".docx", ".pdf", ".csv"}


def get_supabase_client():
    """Create Supabase client from environment variables."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("Error: Set SUPABASE_URL and SUPABASE_KEY environment variables.")
        sys.exit(1)
    return create_client(url, key)


# ---------------------------------------------------------------------------
# Stage 1: File Intake
# ---------------------------------------------------------------------------
def compute_hash(file_path: str) -> str:
    """SHA256 hash of file contents for dedup / change detection."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def scan_source_folder(source_dir: str) -> list[dict]:
    """Walk source_dir and collect supported files."""
    files = []
    source_path = Path(source_dir)
    for file_path in sorted(source_path.rglob("*")):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append({
                "file_name": file_path.name,
                "file_path": str(file_path.resolve()),
                "file_type": file_path.suffix.lstrip(".").lower(),
                "file_size": file_path.stat().st_size,
                "file_hash": compute_hash(str(file_path)),
            })
    return files


def register_files(supabase, files: list[dict]) -> list[dict]:
    """
    Check each file against file_metadata. Returns list of files
    that need processing (new or previously failed).
    """
    to_process = []

    for file_info in files:
        # Check if this hash already exists
        result = (
            supabase.table("file_metadata")
            .select("id, status")
            .eq("file_hash", file_info["file_hash"])
            .execute()
        )

        if result.data:
            row = result.data[0]
            if row["status"] == "completed":
                print(f"  Skip (unchanged): {file_info['file_name']}")
                continue
            elif row["status"] == "failed":
                print(f"  Retry (failed):   {file_info['file_name']}")
                file_info["file_metadata_id"] = row["id"]
                # Reset status to processing
                supabase.table("file_metadata").update(
                    {"status": "processing", "error_message": None}
                ).eq("id", row["id"]).execute()
                to_process.append(file_info)
                continue

        # New file — insert metadata row
        insert_result = (
            supabase.table("file_metadata")
            .insert({
                "file_name": file_info["file_name"],
                "file_path": file_info["file_path"],
                "file_type": file_info["file_type"],
                "file_size": file_info["file_size"],
                "file_hash": file_info["file_hash"],
                "status": "processing",
            })
            .execute()
        )
        file_info["file_metadata_id"] = insert_result.data[0]["id"]
        print(f"  New file:         {file_info['file_name']}")
        to_process.append(file_info)

    return to_process


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="RAG Pipeline — File Intake")
    parser.add_argument(
        "--source-dir",
        default="../source-files",
        help="Path to source files folder (default: ../source-files)",
    )
    parser.add_argument(
        "--output-dir",
        default="./output",
        help="Path to write intermediate JSON files (default: ./output)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Stage 1: File Intake")
    print("=" * 60)

    # Scan source folder
    files = scan_source_folder(args.source_dir)
    print(f"\nFound {len(files)} supported files:")
    for f in files:
        print(f"  {f['file_name']} ({f['file_type']}, {f['file_size']} bytes)")

    # Register with Supabase
    print("\nRegistering with Supabase...")
    supabase = get_supabase_client()
    to_process = register_files(supabase, files)
    print(f"\n{len(to_process)} files to process.")

    if not to_process:
        print("Nothing to process. All files are up to date.")
        return

    # Write file manifest for conversion step
    output_file = output_dir / "registered.json"
    serializable = []
    for f in to_process:
        serializable.append({
            "file_metadata_id": f["file_metadata_id"],
            "file_name": f["file_name"],
            "file_path": f["file_path"],
            "file_type": f["file_type"],
            "file_size": f["file_size"],
        })

    with open(output_file, "w", encoding="utf-8") as fh:
        json.dump(serializable, fh, indent=2)

    print(f"\n{'=' * 60}")
    print(f"Done. {len(to_process)} files registered.")
    print(f"Output: {output_file}")
    print(f"Next step: python convert.py --input {output_file}, then python chunking.py")


if __name__ == "__main__":
    main()
