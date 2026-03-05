"""
Stage 3: Chunking Router
=========================
Reads converted markdown from the ingest step and splits each document
into chunks using a strategy selected by file type. Outputs JSON ready
for the embedding step.

Usage:
    python chunking.py --input ./output/converted.json --output-dir ./output

Prerequisites:
    - pip install tiktoken
"""

import argparse
import json
import re
import sys
from pathlib import Path

import tiktoken

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MAX_CHUNK_TOKENS = 600
OVERLAP_RATIO = 0.12  # ~12% overlap
MIN_CHUNK_TOKENS = 50
CSV_ROW_GROUP_SIZE = 10

# Token counter
_encoding = tiktoken.encoding_for_model("gpt-4")


def count_tokens(text: str) -> int:
    return len(_encoding.encode(text))


# ---------------------------------------------------------------------------
# Chunking Strategies
# ---------------------------------------------------------------------------
def chunk_by_headings(markdown: str, structure: dict) -> list[dict]:
    """
    Split markdown at heading boundaries (##, ###).
    Used for md, docx, and pdf files with heading structure.
    """
    # Split at heading markers
    pattern = r"(^#{1,4}\s+.+$)"
    parts = re.split(pattern, markdown, flags=re.MULTILINE)

    sections = []
    current_heading = None
    current_level = 0
    current_text = ""

    for part in parts:
        part = part.strip()
        if not part:
            continue

        heading_match = re.match(r"^(#{1,4})\s+(.+)$", part)
        if heading_match:
            # Save previous section
            if current_text.strip():
                sections.append({
                    "heading": current_heading,
                    "level": current_level,
                    "text": current_text.strip(),
                })
            current_level = len(heading_match.group(1))
            current_heading = heading_match.group(2).strip()
            current_text = part + "\n\n"
        else:
            current_text += part + "\n\n"

    # Don't forget the last section
    if current_text.strip():
        sections.append({
            "heading": current_heading,
            "level": current_level,
            "text": current_text.strip(),
        })

    # If no headings found, fall back to recursive
    if len(sections) <= 1 and markdown.strip():
        return chunk_recursive(markdown, structure)

    # Now split oversized sections and merge undersized ones
    chunks = []
    for section in sections:
        tokens = count_tokens(section["text"])

        if tokens <= MAX_CHUNK_TOKENS:
            chunks.append({
                "content": section["text"],
                "token_count": tokens,
                "section_heading": section["heading"],
                "hierarchy_level": section["level"],
                "has_table": "|" in section["text"] and "---" in section["text"],
            })
        else:
            # Split large sections at paragraph boundaries
            sub_chunks = split_at_paragraphs(
                section["text"], section["heading"], section["level"]
            )
            chunks.extend(sub_chunks)

    # Merge small chunks with their neighbors
    chunks = merge_small_chunks(chunks)

    # Add overlap between adjacent chunks
    chunks = add_overlap(chunks)

    return chunks


def chunk_csv_rows(markdown: str, structure: dict) -> list[dict]:
    """
    Group CSV rows into chunks, prepending headers to each.
    The markdown at this point is a markdown table.
    """
    lines = [l for l in markdown.strip().split("\n") if l.strip()]

    if len(lines) < 2:
        return [{
            "content": markdown.strip(),
            "token_count": count_tokens(markdown.strip()),
            "section_heading": None,
            "hierarchy_level": 0,
            "has_table": True,
        }]

    header_line = lines[0]
    separator_line = lines[1] if len(lines) > 1 and "---" in lines[1] else None
    data_start = 2 if separator_line else 1
    data_lines = lines[data_start:]

    columns = structure.get("columns", [])
    col_header = ", ".join(columns) if columns else header_line

    chunks = []
    for i in range(0, len(data_lines), CSV_ROW_GROUP_SIZE):
        group = data_lines[i : i + CSV_ROW_GROUP_SIZE]

        # Build readable text block
        chunk_lines = [header_line]
        if separator_line:
            chunk_lines.append(separator_line)
        chunk_lines.extend(group)
        content = "\n".join(chunk_lines)

        chunks.append({
            "content": content,
            "token_count": count_tokens(content),
            "section_heading": f"Rows {i + 1}–{i + len(group)} ({col_header})",
            "hierarchy_level": 0,
            "has_table": True,
        })

    return chunks


def chunk_recursive(markdown: str, structure: dict) -> list[dict]:
    """
    Fallback: split at paragraph boundaries, then sentence boundaries.
    """
    paragraphs = re.split(r"\n\n+", markdown.strip())
    raw_chunks = []
    current = ""

    for para in paragraphs:
        candidate = (current + "\n\n" + para).strip() if current else para.strip()
        if count_tokens(candidate) <= MAX_CHUNK_TOKENS:
            current = candidate
        else:
            if current:
                raw_chunks.append(current)
            # If single paragraph is too big, split at sentences
            if count_tokens(para) > MAX_CHUNK_TOKENS:
                raw_chunks.extend(split_at_sentences(para))
            else:
                current = para
                continue
            current = ""

    if current:
        raw_chunks.append(current)

    chunks = []
    for text in raw_chunks:
        chunks.append({
            "content": text,
            "token_count": count_tokens(text),
            "section_heading": None,
            "hierarchy_level": 0,
            "has_table": "|" in text and "---" in text,
        })

    chunks = merge_small_chunks(chunks)
    chunks = add_overlap(chunks)
    return chunks


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def split_at_paragraphs(text: str, heading: str, level: int) -> list[dict]:
    """Split a large section at paragraph boundaries."""
    paragraphs = re.split(r"\n\n+", text.strip())
    chunks = []
    current = ""

    for para in paragraphs:
        candidate = (current + "\n\n" + para).strip() if current else para.strip()
        if count_tokens(candidate) <= MAX_CHUNK_TOKENS:
            current = candidate
        else:
            if current:
                chunks.append({
                    "content": current,
                    "token_count": count_tokens(current),
                    "section_heading": heading,
                    "hierarchy_level": level,
                    "has_table": "|" in current and "---" in current,
                })
            current = para

    if current:
        chunks.append({
            "content": current,
            "token_count": count_tokens(current),
            "section_heading": heading,
            "hierarchy_level": level,
            "has_table": "|" in current and "---" in current,
        })

    return chunks


def split_at_sentences(text: str) -> list[str]:
    """Split text at sentence boundaries when paragraphs are too big."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    current = ""

    for sentence in sentences:
        candidate = (current + " " + sentence).strip() if current else sentence.strip()
        if count_tokens(candidate) <= MAX_CHUNK_TOKENS:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = sentence

    if current:
        chunks.append(current)

    return chunks


def merge_small_chunks(chunks: list[dict]) -> list[dict]:
    """Merge chunks below MIN_CHUNK_TOKENS with their neighbors."""
    if len(chunks) <= 1:
        return chunks

    merged = [chunks[0]]
    for chunk in chunks[1:]:
        if chunk["token_count"] < MIN_CHUNK_TOKENS and merged:
            # Merge with previous
            prev = merged[-1]
            combined = prev["content"] + "\n\n" + chunk["content"]
            merged[-1] = {
                "content": combined,
                "token_count": count_tokens(combined),
                "section_heading": prev["section_heading"] or chunk["section_heading"],
                "hierarchy_level": prev["hierarchy_level"],
                "has_table": prev["has_table"] or chunk["has_table"],
            }
        else:
            merged.append(chunk)

    return merged


def add_overlap(chunks: list[dict]) -> list[dict]:
    """Add overlap by prepending tail of previous chunk."""
    if len(chunks) <= 1:
        return chunks

    overlap_tokens = int(MAX_CHUNK_TOKENS * OVERLAP_RATIO)
    result = [chunks[0]]

    for i in range(1, len(chunks)):
        prev_text = chunks[i - 1]["content"]
        # Get last N tokens worth of text from previous chunk
        sentences = re.split(r"(?<=[.!?])\s+", prev_text)
        overlap_text = ""
        for s in reversed(sentences):
            candidate = (s + " " + overlap_text).strip() if overlap_text else s
            if count_tokens(candidate) <= overlap_tokens:
                overlap_text = candidate
            else:
                break

        if overlap_text:
            new_content = overlap_text + "\n\n" + chunks[i]["content"]
        else:
            new_content = chunks[i]["content"]

        result.append({
            **chunks[i],
            "content": new_content,
            "token_count": count_tokens(new_content),
        })

    return result


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
def select_strategy(markdown: str, file_type: str):
    """Pick chunking strategy based on content signals, not just extension."""
    if file_type == "csv":
        return chunk_csv_rows

    headings = len(re.findall(r"^#{1,4}\s+", markdown, re.MULTILINE))
    table_rows = len(re.findall(r"^\|.+\|$", markdown, re.MULTILINE))
    total_lines = len(markdown.strip().split("\n"))

    if total_lines > 0 and table_rows > total_lines * 0.5:
        return chunk_csv_rows

    if headings >= 3:
        return chunk_by_headings

    return chunk_recursive


def chunk_file(file_data: dict) -> tuple[list[dict], str]:
    """Route a file to the appropriate chunking strategy."""
    strategy = select_strategy(file_data["markdown"], file_data["file_type"])
    chunks = strategy(file_data["markdown"], file_data.get("structure", {}))

    # Assign chunk indexes
    for i, chunk in enumerate(chunks):
        chunk["chunk_index"] = i

    return chunks, strategy.__name__


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="RAG Pipeline — Chunking Router")
    parser.add_argument(
        "--input",
        default="./output/converted.json",
        help="Path to converted.json from ingest step",
    )
    parser.add_argument(
        "--output-dir",
        default="./output",
        help="Path to write chunked output (default: ./output)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        print("Run ingest.py first.")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        files = json.load(f)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Stage 3: Chunking Router")
    print("=" * 60)

    all_chunked = []
    total_chunks = 0

    for file_data in files:
        print(f"\n  Chunking: {file_data['file_name']} ({file_data['file_type']})...", end=" ")

        chunks, strategy_name = chunk_file(file_data)
        total_chunks += len(chunks)

        token_counts = [c["token_count"] for c in chunks]
        avg_tokens = sum(token_counts) / len(token_counts) if token_counts else 0

        print(
            f"{len(chunks)} chunks "
            f"(avg {avg_tokens:.0f} tokens, strategy: {strategy_name})"
        )

        all_chunked.append({
            "file_metadata_id": file_data["file_metadata_id"],
            "file_name": file_data["file_name"],
            "file_type": file_data["file_type"],
            "chunk_strategy": strategy_name,
            "chunks": chunks,
        })

    # Verify chunks
    warnings = 0
    for file_rec in all_chunked:
        for chunk in file_rec["chunks"]:
            label = f"{file_rec['file_name']} chunk {chunk['chunk_index']}"

            if not chunk["content"].strip():
                print(f"  WARNING: {label} is empty")
                warnings += 1

            if chunk["token_count"] > MAX_CHUNK_TOKENS * 1.5:
                print(f"  WARNING: {label} is oversized ({chunk['token_count']} tokens)")
                warnings += 1

            if chunk["has_table"]:
                lines = chunk["content"].strip().split("\n")
                table_lines = [l for l in lines if l.strip().startswith("|")]
                has_header_sep = any("---" in l for l in table_lines)
                if table_lines and not has_header_sep:
                    print(f"  WARNING: {label} has table rows without a header")
                    warnings += 1

    if warnings:
        print(f"\n  {warnings} warning(s) found — review above before embedding.")

    # Write output
    output_file = output_dir / "chunked.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunked, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"Done. {total_chunks} total chunks from {len(files)} files.")
    print(f"Output: {output_file}")
    print(f"Next step: python embed.py --input {output_file}")


if __name__ == "__main__":
    main()
