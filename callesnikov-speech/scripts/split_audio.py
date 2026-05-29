#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Split source audio into stable 50-70 second chunks.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--output", default="splitted_records", type=Path)
    args = parser.parse_args()

    if args.seconds < 50 or args.seconds > 70:
        raise SystemExit("--seconds must be in the 50-70 range")
    source = args.source.resolve()
    if not source.exists():
        raise SystemExit(f"source file not found: {source}")

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    pattern = output / "audioChunk_%03d.wav"

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-y",
        "-i",
        str(source),
        "-f",
        "segment",
        "-segment_time",
        str(args.seconds),
        "-reset_timestamps",
        "1",
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(pattern),
    ]
    subprocess.run(cmd, check=True)
    chunks = sorted(output.glob("audioChunk_*.wav"))
    print(f"split {source} into {len(chunks)} chunk(s) in {output}")


if __name__ == "__main__":
    main()
