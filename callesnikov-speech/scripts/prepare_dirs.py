#!/usr/bin/env python3
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Create transcription output directories.")
    parser.add_argument("--workdir", default=".", type=Path)
    args = parser.parse_args()

    workdir = args.workdir.resolve()
    for dirname in ["transferred", "low_merged"]:
        path = workdir / dirname
        path.mkdir(parents=True, exist_ok=True)
        print(path)


if __name__ == "__main__":
    main()
