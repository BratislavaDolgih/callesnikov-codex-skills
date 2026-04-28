#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


CHUNK_RE = re.compile(r"audioChunk_(\d+)\.txt$", re.IGNORECASE)


def chunk_number(path):
    match = CHUNK_RE.search(path.name)
    return int(match.group(1)) if match else None


def main():
    parser = argparse.ArgumentParser(description="Merge transcript txt chunks into larger files.")
    parser.add_argument("--workdir", default=".", type=Path)
    parser.add_argument("--input", default="transferred", type=Path)
    parser.add_argument("--output", default="low_merged", type=Path)
    parser.add_argument("--batch-size", default=20, type=int)
    args = parser.parse_args()

    if args.batch_size < 20 or args.batch_size > 30:
        raise SystemExit("--batch-size must be in the 20-30 range")

    workdir = args.workdir.resolve()
    input_dir = args.input if args.input.is_absolute() else workdir / args.input
    output_dir = args.output if args.output.is_absolute() else workdir / args.output
    if not input_dir.exists():
        raise SystemExit(f"input directory not found: {input_dir}")

    numbered = [(chunk_number(path), path) for path in input_dir.glob("audioChunk_*.txt")]
    chunks = [(number, path) for number, path in numbered if number is not None]
    chunks.sort(key=lambda item: item[0])
    if not chunks:
        raise SystemExit(f"no audioChunk_*.txt files found in {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for start in range(0, len(chunks), args.batch_size):
        group = chunks[start : start + args.batch_size]
        first = group[0][0]
        last = group[-1][0]
        target = output_dir / f"mergedFrom{first}To{last}.txt"
        text_parts = []
        for _, path in group:
            text_parts.append(path.read_text(encoding="utf-8", errors="replace").strip())
        target.write_text("\n\n".join(part for part in text_parts if part) + "\n", encoding="utf-8")
        written.append(target)
        print(target)

    print(f"merged {len(chunks)} chunk(s) into {len(written)} file(s)")


if __name__ == "__main__":
    main()
