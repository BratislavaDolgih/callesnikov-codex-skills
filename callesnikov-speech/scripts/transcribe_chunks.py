#!/usr/bin/env python3
import argparse
import shutil
import subprocess
from pathlib import Path


def find_whisper_binary(skill_root):
    local_names = ["whisper-cli.exe", "main.exe", "whisper-cli", "main"]
    path_names = ["whisper-cli.exe", "whisper-cli", "main.exe"]
    for base in [
        skill_root / "runtime" / "whisper.cpp",
        skill_root / "runtime" / "whisper.cpp" / "build",
        skill_root / "runtime" / "whisper.cpp" / "build" / "bin",
    ]:
        if base.exists():
            for name in local_names:
                matches = list(base.rglob(name))
                if matches:
                    return matches[0]
    for name in path_names:
        found = shutil.which(name)
        if found:
            return Path(found)
    return None


def main():
    parser = argparse.ArgumentParser(description="Transcribe chunked audio with whisper.cpp.")
    parser.add_argument("--workdir", default=".", type=Path)
    parser.add_argument("--skill-root", default=Path(__file__).resolve().parents[1], type=Path)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--input", default="splitted_records", type=Path)
    parser.add_argument("--output", default="transferred", type=Path)
    args = parser.parse_args()

    workdir = args.workdir.resolve()
    skill_root = args.skill_root.resolve()
    model = args.model or skill_root / "runtime" / "whisper.cpp" / "models" / "ggml-large-v3-turbo.bin"
    binary = args.binary or find_whisper_binary(skill_root)
    input_dir = args.input if args.input.is_absolute() else workdir / args.input
    output_dir = args.output if args.output.is_absolute() else workdir / args.output

    if not binary:
        raise SystemExit("whisper.cpp binary not found")
    if not model.exists():
        raise SystemExit(f"model not found: {model}")
    if not input_dir.exists():
        raise SystemExit(f"chunk directory not found: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    chunks = sorted(input_dir.glob("audioChunk_*.wav"))
    if not chunks:
        raise SystemExit(f"no audioChunk_*.wav files found in {input_dir}")

    for chunk in chunks:
        out_base = output_dir / chunk.stem
        cmd = [
            str(binary),
            "-m",
            str(model),
            "-f",
            str(chunk),
            "-of",
            str(out_base),
            "-oj",
            "-osrt",
            "-otxt",
        ]
        subprocess.run(cmd, check=True)
        print(f"transcribed {chunk.name}")


if __name__ == "__main__":
    main()
