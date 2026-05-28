#!/usr/bin/env python3
"""
Kolesnikov YouTube Preserver.

Robust yt-dlp wrapper for saving single YouTube videos or audio tracks from Codex.
It does not install packages globally. Install or update yt-dlp separately when needed.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


QUALITY_CHOICES = ["best", "2160p", "1440p", "1080p", "720p", "480p", "360p", "worst"]
FORMAT_CHOICES = ["mp4", "webm", "mkv"]


def resolve_yt_dlp() -> list[str]:
    exe = shutil.which("yt-dlp")
    if exe:
        return [exe]

    try:
        subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [sys.executable, "-m", "yt_dlp"]
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise SystemExit(
            "yt-dlp is not available. Install it locally or put yt-dlp on PATH; "
            "this script intentionally does not run global pip installs."
        )


def run(cmd: list[str], *, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=capture,
    )


def get_video_info(yt_dlp: list[str], url: str, no_playlist: bool) -> dict:
    cmd = yt_dlp + ["--dump-json"]
    if no_playlist:
        cmd.append("--no-playlist")
    cmd.append(url)
    result = run(cmd, capture=True)
    first_json_line = next((line for line in result.stdout.splitlines() if line.strip()), "{}")
    return json.loads(first_json_line)


def format_selector(quality: str, container: str) -> str:
    if quality == "best":
        if container == "mp4":
            return "bv*[ext=mp4]+ba[ext=m4a]/bv*+ba/best"
        return "bv*+ba/best"
    if quality == "worst":
        return "wv*+wa/worst"

    height = quality.removesuffix("p")
    if container == "mp4":
        return f"bv*[height<={height}][ext=mp4]+ba[ext=m4a]/bv*[height<={height}]+ba/b[height<={height}]/best[height<={height}]"
    return f"bv*[height<={height}]+ba/b[height<={height}]/best[height<={height}]"


def build_command(args: argparse.Namespace, yt_dlp: list[str], output_dir: Path) -> list[str]:
    output_template = str(output_dir / "%(title).200B [%(id)s].%(ext)s")
    cmd = yt_dlp + [
        "--windows-filenames",
        "--trim-filenames",
        "200",
        "--restrict-filenames",
        "--no-mtime",
        "--retries",
        str(args.retries),
        "--fragment-retries",
        str(args.fragment_retries),
        "--concurrent-fragments",
        str(args.concurrent_fragments),
        "-o",
        output_template,
    ]

    if not args.playlist:
        cmd.append("--no-playlist")

    if args.no_overwrites:
        cmd.append("--no-overwrites")

    if args.write_info_json:
        cmd.append("--write-info-json")

    if args.write_thumbnail:
        cmd.append("--write-thumbnail")

    if args.write_subs:
        cmd.extend(["--write-subs", "--write-auto-subs", "--sub-langs", args.sub_langs])

    if args.cookies_from_browser:
        cmd.extend(["--cookies-from-browser", args.cookies_from_browser])

    if args.audio_only:
        cmd.extend(["-x", "--audio-format", args.audio_format, "--audio-quality", "0"])
        if args.keep_intermediate:
            cmd.append("--keep-video")
    else:
        cmd.extend(["-f", format_selector(args.quality, args.format), "--merge-output-format", args.format])

    cmd.append(args.url)
    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(description="Preserve YouTube videos or audio with yt-dlp.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output", type=Path, default=Path.cwd() / "downloads" / "youtube-preserver")
    parser.add_argument("-q", "--quality", default="best", choices=QUALITY_CHOICES)
    parser.add_argument("-f", "--format", default="mp4", choices=FORMAT_CHOICES)
    parser.add_argument("-a", "--audio-only", action="store_true", help="Extract audio only")
    parser.add_argument("--audio-format", default="mp3", choices=["mp3", "m4a", "opus", "wav", "flac"])
    parser.add_argument("--playlist", action="store_true", help="Allow playlist downloads; default is single-video only")
    parser.add_argument("--write-info-json", action="store_true", help="Save yt-dlp metadata JSON")
    parser.add_argument("--write-thumbnail", action="store_true", help="Save thumbnail")
    parser.add_argument("--write-subs", action="store_true", help="Save subtitles and auto subtitles")
    parser.add_argument("--sub-langs", default="en,ru,uk,ja,ko,zh.*", help="Subtitle language selector")
    parser.add_argument("--cookies-from-browser", help="Pass browser name to yt-dlp, e.g. chrome or firefox")
    parser.add_argument("--no-overwrites", action="store_true", help="Do not overwrite existing files")
    parser.add_argument("--keep-intermediate", action="store_true", help="Keep original media after audio extraction")
    parser.add_argument("--retries", type=int, default=10)
    parser.add_argument("--fragment-retries", type=int, default=10)
    parser.add_argument("--concurrent-fragments", type=int, default=4)

    args = parser.parse_args()
    output_dir = args.output.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    yt_dlp = resolve_yt_dlp()
    print(f"yt-dlp: {' '.join(yt_dlp)}")
    print(f"output: {output_dir}")

    try:
        info = get_video_info(yt_dlp, args.url, no_playlist=not args.playlist)
        duration = info.get("duration")
        duration_text = f"{duration // 60}:{duration % 60:02d}" if isinstance(duration, int) else "unknown"
        print(f"title: {info.get('title', 'unknown')}")
        print(f"uploader: {info.get('uploader') or info.get('channel') or 'unknown'}")
        print(f"duration: {duration_text}")

        cmd = build_command(args, yt_dlp, output_dir)
        print("command:", " ".join(f'"{part}"' if " " in part else part for part in cmd))
        run(cmd)
    except subprocess.CalledProcessError as exc:
        print(f"yt-dlp failed with exit code {exc.returncode}", file=sys.stderr)
        if exc.stdout:
            print(exc.stdout, file=sys.stderr)
        if exc.stderr:
            print(exc.stderr, file=sys.stderr)
        return exc.returncode or 1
    except json.JSONDecodeError as exc:
        print(f"Could not decode yt-dlp metadata JSON: {exc}", file=sys.stderr)
        return 1

    files = sorted(p for p in output_dir.iterdir() if p.is_file())
    print("\nSaved files:")
    for path in files:
        print(f"- {path} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
