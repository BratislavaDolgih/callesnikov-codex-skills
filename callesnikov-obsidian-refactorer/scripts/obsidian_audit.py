#!/usr/bin/env python3
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


IGNORED_DIRS = {".git", ".obsidian", ".trash", "node_modules", "__pycache__"}
TEXT_EXTS = {".md", ".canvas"}
ATTACHMENT_EXTS = {
    ".avif",
    ".bmp",
    ".gif",
    ".jpeg",
    ".jpg",
    ".m4a",
    ".mp3",
    ".mp4",
    ".ogg",
    ".pdf",
    ".png",
    ".svg",
    ".webm",
    ".wav",
    ".webp",
}
WIKI_RE = re.compile(r"(!?)\[\[([^\]\n]+)\]\]")
NUMERIC_PREFIX_RE = re.compile(r"^\s*(?:\d+[.\-_ )]+)+\s*")


def is_ignored(path):
    return any(part in IGNORED_DIRS for part in path.parts)


def iter_files(vault):
    for path in vault.rglob("*"):
        if path.is_file() and not is_ignored(path.relative_to(vault)):
            yield path


def decode_text(path):
    data = path.read_bytes()
    has_bom = data.startswith(b"\xef\xbb\xbf")
    try:
        text = data.decode("utf-8-sig" if has_bom else "utf-8")
        return text, {
            "ok": True,
            "has_bom": has_bom,
            "error": None,
            "mixed_line_endings": b"\r\n" in data and b"\n" in data.replace(b"\r\n", b""),
        }
    except UnicodeDecodeError as exc:
        return "", {
            "ok": False,
            "has_bom": has_bom,
            "error": str(exc),
            "mixed_line_endings": False,
        }


def strip_code_blocks(text):
    result = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```") or line.lstrip().startswith("~~~"):
            in_fence = not in_fence
            result.append("\n")
        elif in_fence:
            result.append("\n")
        else:
            result.append(line)
    return "".join(result)


def parse_link(raw):
    target = raw.strip()
    alias = None
    heading = None
    if "|" in target:
        target, alias = target.split("|", 1)
    if "#" in target:
        target, heading = target.split("#", 1)
    return {
        "target": target.strip(),
        "alias": alias,
        "heading": heading,
        "basename": Path(target.strip()).stem if target.strip() else "",
    }


def normalized_title(name):
    stem = Path(name).stem
    return NUMERIC_PREFIX_RE.sub("", stem).strip().lower()


def build_index(vault):
    by_basename = defaultdict(list)
    by_stem = defaultdict(list)
    by_normalized = defaultdict(list)
    for path in iter_files(vault):
        rel = path.relative_to(vault).as_posix()
        suffix = path.suffix.lower()
        if suffix in TEXT_EXTS or suffix in ATTACHMENT_EXTS:
            by_basename[path.name].append(rel)
            by_stem[path.stem].append(rel)
            norm = normalized_title(path.stem)
            if norm:
                by_normalized[norm].append(rel)
    return by_basename, by_stem, by_normalized


def resolve_target(parsed, by_basename, by_stem, by_normalized):
    target = parsed["target"]
    if not target:
        return "empty", []

    target_path = Path(target)
    candidates = []
    if target_path.name in by_basename:
        candidates = by_basename[target_path.name]
    elif target_path.stem in by_stem:
        candidates = by_stem[target_path.stem]
    elif parsed["basename"] in by_stem:
        candidates = by_stem[parsed["basename"]]
    else:
        norm = normalized_title(parsed["basename"])
        candidates = by_normalized.get(norm, [])

    if len(candidates) == 1:
        return "resolved", candidates
    if len(candidates) > 1:
        return "ambiguous", candidates
    return "unresolved", []


def scope_files(vault, scope):
    if scope:
        scoped = (vault / scope).resolve()
        if not scoped.exists():
            raise SystemExit(f"scope not found: {scoped}")
        if scoped.is_file():
            return [scoped] if scoped.suffix.lower() in TEXT_EXTS else []
        roots = [scoped]
    else:
        roots = [vault]

    files = []
    for root in roots:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_EXTS and not is_ignored(path.relative_to(vault)):
                files.append(path)
    return sorted(files)


def audit(vault, scope=None, include_code_blocks=False):
    vault = vault.resolve()
    by_basename, by_stem, by_normalized = build_index(vault)
    report = {
        "vault": str(vault),
        "scope": scope or ".",
        "files_checked": 0,
        "links_checked": 0,
        "encoding_issues": [],
        "frontmatter_issues": [],
        "unresolved_links": [],
        "ambiguous_links": [],
    }

    for path in scope_files(vault, scope):
        rel = path.relative_to(vault).as_posix()
        text, encoding = decode_text(path)
        report["files_checked"] += 1
        if not encoding["ok"] or encoding["has_bom"] or encoding["mixed_line_endings"]:
            report["encoding_issues"].append({"file": rel, **encoding})
        if text.startswith("---") and "\n---" not in text[3:]:
            report["frontmatter_issues"].append({"file": rel, "issue": "frontmatter opening delimiter without closing delimiter"})
        if not encoding["ok"]:
            continue

        scan_text = text if include_code_blocks else strip_code_blocks(text)
        for match in WIKI_RE.finditer(scan_text):
            report["links_checked"] += 1
            parsed = parse_link(match.group(2))
            status, candidates = resolve_target(parsed, by_basename, by_stem, by_normalized)
            item = {
                "file": rel,
                "token": match.group(0),
                "embed": bool(match.group(1)),
                "target": parsed["target"],
            }
            if status == "unresolved":
                report["unresolved_links"].append(item)
            elif status == "ambiguous":
                item["candidates"] = candidates
                report["ambiguous_links"].append(item)
    return report


def markdown_report(report):
    lines = [
        "# Obsidian Audit",
        "",
        f"- Vault: `{report['vault']}`",
        f"- Scope: `{report['scope']}`",
        f"- Files checked: {report['files_checked']}",
        f"- Links checked: {report['links_checked']}",
        f"- Encoding issues: {len(report['encoding_issues'])}",
        f"- Frontmatter issues: {len(report['frontmatter_issues'])}",
        f"- Unresolved links: {len(report['unresolved_links'])}",
        f"- Ambiguous links: {len(report['ambiguous_links'])}",
        "",
    ]
    for title, key in [
        ("Encoding Issues", "encoding_issues"),
        ("Frontmatter Issues", "frontmatter_issues"),
        ("Unresolved Links", "unresolved_links"),
        ("Ambiguous Links", "ambiguous_links"),
    ]:
        if report[key]:
            lines.extend([f"## {title}", ""])
            for item in report[key]:
                lines.append(f"- `{item.get('file')}`: `{item.get('token') or item.get('issue') or item.get('error')}`")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Audit an Obsidian vault for encoding and wiki-link issues.")
    parser.add_argument("vault", type=Path)
    parser.add_argument("--scope", help="Relative folder or note path to inspect.")
    parser.add_argument("--include-code-blocks", action="store_true")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if not args.vault.exists() or not args.vault.is_dir():
        raise SystemExit(f"vault directory not found: {args.vault}")

    report = audit(args.vault, args.scope, args.include_code_blocks)
    if args.format == "markdown":
        rendered = markdown_report(report)
    else:
        rendered = json.dumps(report, indent=2, ensure_ascii=False)

    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
        if not rendered.endswith("\n"):
            sys.stdout.write("\n")


if __name__ == "__main__":
    main()
