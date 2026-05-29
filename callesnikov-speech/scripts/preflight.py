#!/usr/bin/env python3
import argparse
import json
import shutil
import sys
from pathlib import Path


def find_whisper_binary(root):
    local_names = ["whisper-cli.exe", "main.exe", "whisper-cli", "main"]
    path_names = ["whisper-cli.exe", "whisper-cli", "main.exe"]
    search_roots = [
        root / "runtime" / "whisper.cpp",
        root / "runtime" / "whisper.cpp" / "build",
        root / "runtime" / "whisper.cpp" / "build" / "bin",
    ]
    for search_root in search_roots:
        if not search_root.exists():
            continue
        for name in local_names:
            matches = list(search_root.rglob(name))
            if matches:
                return matches[0]
    for name in path_names:
        found = shutil.which(name)
        if found:
            return Path(found)
    return None


def main():
    parser = argparse.ArgumentParser(description="Check local ffmpeg/whisper.cpp transcription prerequisites.")
    parser.add_argument("--skill-root", default=Path(__file__).resolve().parents[1], type=Path)
    args = parser.parse_args()

    skill_root = args.skill_root.resolve()
    model_dir = skill_root / "runtime" / "whisper.cpp" / "models"
    default_model = model_dir / "ggml-large-v3-turbo.bin"
    whisper_binary = find_whisper_binary(skill_root)

    checks = {
        "skill_root": str(skill_root),
        "ffmpeg": shutil.which("ffmpeg"),
        "python": sys.executable,
        "cmake": shutil.which("cmake"),
        "whisper_binary": str(whisper_binary) if whisper_binary else None,
        "model_dir": str(model_dir),
        "default_model": str(default_model) if default_model.exists() else None,
        "available_models": [str(p) for p in sorted(model_dir.glob("ggml*.bin"))] if model_dir.exists() else [],
        "official_runtime_source": "https://github.com/ggml-org/whisper.cpp",
    }
    checks["ok"] = bool(checks["ffmpeg"] and checks["python"] and checks["cmake"] and checks["whisper_binary"] and checks["available_models"])

    print(json.dumps(checks, indent=2))
    return 0 if checks["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
