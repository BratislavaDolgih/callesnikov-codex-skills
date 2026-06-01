from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


try:
    import pypdf
    from pypdf import PdfReader, PdfWriter
    from pypdf.errors import PdfReadError
except ImportError as exc:
    pypdf = None
    PdfReader = None
    PdfWriter = None
    PdfReadError = Exception
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None


PDF_MAGIC = b"%PDF-"
METADATA_FLAGS = {
    "title": "/Title",
    "author": "/Author",
    "subject": "/Subject",
    "keywords": "/Keywords",
    "creator": "/Creator",
    "producer": "/Producer",
}


def require_pypdf() -> None:
    if IMPORT_ERROR is not None:
        raise RuntimeError(
            "Missing dependency: pypdf. Install with: "
            "python -m pip install -r scripts/requirements.txt"
        )


def resolve_output(path: str | Path, *, force: bool = False) -> Path:
    out = Path(path)
    if not out.is_absolute():
        out = Path.cwd() / out
    if out.exists() and not force:
        raise FileExistsError(f"Output already exists: {out}. Use --force to overwrite.")
    out.parent.mkdir(parents=True, exist_ok=True)
    return out


def require_file(path: str | Path) -> Path:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {p}")
    if not p.is_file():
        raise ValueError(f"Input is not a file: {p}")
    return p


def has_pdf_header(path: Path) -> bool:
    with path.open("rb") as fh:
        return fh.read(5) == PDF_MAGIC


def reader_for(path: str | Path, password: str | None = None):
    require_pypdf()
    p = require_file(path)
    reader = PdfReader(str(p), strict=False)
    if reader.is_encrypted:
        if not password:
            raise ValueError(f"PDF is encrypted and needs --password: {p}")
        result = reader.decrypt(password)
        if result == 0:
            raise ValueError("Could not decrypt PDF with provided password")
    return reader


def parse_pages(spec: str | None, total: int) -> list[int]:
    if spec is None or spec.strip().lower() == "all":
        return list(range(total))
    spec = spec.strip().lower()
    if spec == "odd":
        return list(range(0, total, 2))
    if spec == "even":
        return list(range(1, total, 2))

    indexes: list[int] = []
    seen: set[int] = set()
    for part in spec.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start_s, end_s = token.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if start > end:
                raise ValueError(f"Invalid descending range: {token}")
            nums = range(start, end + 1)
        else:
            nums = [int(token)]
        for num in nums:
            if num < 1 or num > total:
                raise ValueError(f"Page {num} out of range 1-{total}")
            idx = num - 1
            if idx not in seen:
                indexes.append(idx)
                seen.add(idx)
    if not indexes:
        raise ValueError("No pages selected")
    return indexes


def add_selected_pages(writer, reader, indexes: Iterable[int]) -> None:
    for idx in indexes:
        writer.add_page(reader.pages[idx])


def copy_metadata(reader, writer) -> None:
    if getattr(reader, "metadata", None):
        writer.add_metadata(reader.metadata)


def write_pdf(writer, output: Path, *, manifest: dict[str, Any] | None, no_manifest: bool) -> dict[str, Any]:
    writer.write(str(output))
    result = {
        "output": str(output),
        "output_pages": _safe_page_count(output),
        "bytes": output.stat().st_size,
        "pdf_header": has_pdf_header(output),
    }
    if manifest:
        result.update(manifest)
    PdfReader(str(output), strict=False)
    if not no_manifest:
        manifest_path = output.with_suffix(output.suffix + ".manifest.json")
        safe_manifest = {k: v for k, v in result.items() if "password" not in k.lower()}
        safe_manifest["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
        manifest_path.write_text(json.dumps(safe_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        result["manifest"] = str(manifest_path)
    return result


def _safe_page_count(path: Path) -> int | None:
    try:
        return len(PdfReader(str(path), strict=False).pages)
    except Exception:
        return None


def cmd_self_check(args) -> dict[str, Any]:
    require_pypdf()
    try:
        import cryptography  # noqa: F401
    except ImportError:
        crypto_available = False
    else:
        crypto_available = True
    return {
        "ok": True,
        "pypdf_version": pypdf.__version__,
        "python": sys.version.split()[0],
        "crypto_available": crypto_available,
        "crypto_note": "AES encryption needs cryptography; install scripts/requirements.txt if false.",
    }


def cmd_info(args) -> dict[str, Any]:
    reader = reader_for(args.input, args.password)
    path = require_file(args.input)
    meta = reader.metadata or {}
    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "pdf_header": has_pdf_header(path),
        "pages": len(reader.pages),
        "encrypted": reader.is_encrypted,
        "metadata": {str(k): str(v) for k, v in dict(meta).items()},
        "page_labels": list(getattr(reader, "page_labels", []) or []),
    }


def cmd_extract(args) -> dict[str, Any]:
    reader = reader_for(args.input, args.password)
    indexes = parse_pages(args.pages, len(reader.pages))
    writer = PdfWriter()
    add_selected_pages(writer, reader, indexes)
    copy_metadata(reader, writer)
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={"operation": "extract", "input": str(args.input), "selected_pages": [i + 1 for i in indexes]},
        no_manifest=args.no_manifest,
    )


def cmd_delete(args) -> dict[str, Any]:
    reader = reader_for(args.input, args.password)
    delete_indexes = set(parse_pages(args.pages, len(reader.pages)))
    writer = PdfWriter()
    keep = [i for i in range(len(reader.pages)) if i not in delete_indexes]
    add_selected_pages(writer, reader, keep)
    copy_metadata(reader, writer)
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={"operation": "delete", "input": str(args.input), "deleted_pages": [i + 1 for i in sorted(delete_indexes)]},
        no_manifest=args.no_manifest,
    )


def cmd_merge(args) -> dict[str, Any]:
    writer = PdfWriter()
    inputs = []
    for item in args.inputs:
        reader = reader_for(item)
        writer.append(reader, import_outline=not args.no_outlines)
        inputs.append({"path": str(item), "pages": len(reader.pages)})
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={"operation": "merge", "inputs": inputs},
        no_manifest=args.no_manifest,
    )


def cmd_replace(args) -> dict[str, Any]:
    source = reader_for(args.source, args.password)
    replacement = reader_for(args.replacement, args.replacement_password)
    replace_indexes = set(parse_pages(args.pages, len(source.pages)))
    first = min(replace_indexes)
    last = max(replace_indexes)
    if replace_indexes != set(range(first, last + 1)):
        raise ValueError("replace requires one contiguous page range")

    writer = PdfWriter()
    add_selected_pages(writer, source, range(0, first))
    add_selected_pages(writer, replacement, range(len(replacement.pages)))
    add_selected_pages(writer, source, range(last + 1, len(source.pages)))
    copy_metadata(source, writer)
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={
            "operation": "replace",
            "source": str(args.source),
            "replacement": str(args.replacement),
            "replaced_pages": [first + 1, last + 1],
            "source_pages": len(source.pages),
            "replacement_pages": len(replacement.pages),
            "expected_output_pages": len(source.pages) - (last - first + 1) + len(replacement.pages),
        },
        no_manifest=args.no_manifest,
    )


def cmd_insert(args) -> dict[str, Any]:
    source = reader_for(args.source, args.password)
    insert = reader_for(args.insert, args.insert_password)
    if args.before is not None and args.after is not None:
        raise ValueError("Use only one of --before or --after")
    if args.before is None and args.after is None:
        raise ValueError("Provide --before PAGE or --after PAGE")

    if args.before is not None:
        if args.before < 1 or args.before > len(source.pages) + 1:
            raise ValueError(f"--before must be in 1-{len(source.pages) + 1}")
        pos = args.before - 1
    else:
        if args.after < 0 or args.after > len(source.pages):
            raise ValueError(f"--after must be in 0-{len(source.pages)}")
        pos = args.after

    writer = PdfWriter()
    add_selected_pages(writer, source, range(0, pos))
    add_selected_pages(writer, insert, range(len(insert.pages)))
    add_selected_pages(writer, source, range(pos, len(source.pages)))
    copy_metadata(source, writer)
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={"operation": "insert", "source": str(args.source), "insert": str(args.insert), "position_after_zero_based": pos},
        no_manifest=args.no_manifest,
    )


def cmd_rotate(args) -> dict[str, Any]:
    if args.degrees % 90 != 0:
        raise ValueError("Rotation degrees must be a multiple of 90")
    reader = reader_for(args.input, args.password)
    indexes = set(parse_pages(args.pages, len(reader.pages)))
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        new_page = page
        if i in indexes:
            new_page = new_page.rotate(args.degrees)
        writer.add_page(new_page)
    copy_metadata(reader, writer)
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={"operation": "rotate", "input": str(args.input), "degrees": args.degrees, "pages": [i + 1 for i in sorted(indexes)]},
        no_manifest=args.no_manifest,
    )


def cmd_crop(args) -> dict[str, Any]:
    reader = reader_for(args.input, args.password)
    indexes = set(parse_pages(args.pages, len(reader.pages)))
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        if i in indexes:
            box = page.cropbox
            box.lower_left = (float(box.left) + args.left, float(box.bottom) + args.bottom)
            box.upper_right = (float(box.right) - args.right, float(box.top) - args.top)
        writer.add_page(page)
    copy_metadata(reader, writer)
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={"operation": "crop", "input": str(args.input), "pages": [i + 1 for i in sorted(indexes)]},
        no_manifest=args.no_manifest,
    )


def cmd_stamp(args) -> dict[str, Any]:
    reader = reader_for(args.input, args.password)
    stamp_reader = reader_for(args.stamp, args.stamp_password)
    if len(stamp_reader.pages) < 1:
        raise ValueError("Stamp PDF has no pages")
    stamp_page = stamp_reader.pages[0]
    indexes = set(parse_pages(args.pages, len(reader.pages)))
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        if i in indexes:
            if args.mode == "over":
                page.merge_page(stamp_page)
                writer.add_page(page)
            else:
                under = stamp_page
                under.merge_page(page)
                writer.add_page(under)
        else:
            writer.add_page(page)
    copy_metadata(reader, writer)
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={"operation": "stamp", "input": str(args.input), "stamp": str(args.stamp), "mode": args.mode},
        no_manifest=args.no_manifest,
    )


def cmd_encrypt(args) -> dict[str, Any]:
    reader = reader_for(args.input, args.password)
    writer = PdfWriter(clone_from=reader)
    writer.encrypt(args.new_password, owner_password=args.owner_password, algorithm=args.algorithm)
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={"operation": "encrypt", "input": str(args.input), "algorithm": args.algorithm},
        no_manifest=args.no_manifest,
    )


def cmd_decrypt(args) -> dict[str, Any]:
    reader = reader_for(args.input, args.password)
    writer = PdfWriter()
    add_selected_pages(writer, reader, range(len(reader.pages)))
    copy_metadata(reader, writer)
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={"operation": "decrypt", "input": str(args.input)},
        no_manifest=args.no_manifest,
    )


def cmd_metadata(args) -> dict[str, Any]:
    return cmd_info(args)["metadata"]


def cmd_set_metadata(args) -> dict[str, Any]:
    reader = reader_for(args.input, args.password)
    writer = PdfWriter()
    add_selected_pages(writer, reader, range(len(reader.pages)))
    if not args.clear and reader.metadata:
        writer.add_metadata(reader.metadata)
    metadata = {}
    for attr, pdf_key in METADATA_FLAGS.items():
        value = getattr(args, attr)
        if value is not None:
            metadata[pdf_key] = value
    if metadata:
        writer.add_metadata(metadata)
    elif args.clear:
        writer.metadata = {}
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={"operation": "set-metadata", "input": str(args.input), "changed_fields": list(metadata.keys()), "cleared": args.clear},
        no_manifest=args.no_manifest,
    )


def cmd_list_fields(args) -> dict[str, Any]:
    reader = reader_for(args.input, args.password)
    fields = reader.get_fields() or {}
    return {
        "input": str(args.input),
        "field_count": len(fields),
        "fields": {name: str(field.get("/V", "")) for name, field in fields.items()},
    }


def cmd_fill_form(args) -> dict[str, Any]:
    reader = reader_for(args.input, args.password)
    fields_path = require_file(args.fields_json)
    field_values = json.loads(fields_path.read_text(encoding="utf-8"))
    if not isinstance(field_values, dict):
        raise ValueError("fields_json must contain an object mapping field names to values")
    writer = PdfWriter()
    writer.append(reader)
    targets = writer.pages if args.all_pages else [writer.pages[0]]
    for page in targets:
        writer.update_page_form_field_values(page, field_values, auto_regenerate=False, flatten=args.flatten)
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={"operation": "fill-form", "input": str(args.input), "fields_json": str(fields_path), "flatten": args.flatten},
        no_manifest=args.no_manifest,
    )


def cmd_attach(args) -> dict[str, Any]:
    reader = reader_for(args.input, args.password)
    writer = PdfWriter(clone_from=reader)
    attached = []
    for item in args.files:
        path = require_file(item)
        writer.add_attachment(path.name, path.read_bytes())
        attached.append(str(path))
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={"operation": "attach", "input": str(args.input), "files": attached},
        no_manifest=args.no_manifest,
    )


def cmd_extract_attachments(args) -> dict[str, Any]:
    reader = reader_for(args.input, args.password)
    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = Path.cwd() / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    attachments = getattr(reader, "attachments", {}) or {}
    for name, payloads in attachments.items():
        if isinstance(payloads, (bytes, bytearray)):
            payloads = [payloads]
        for idx, data in enumerate(payloads, start=1):
            suffix = "" if len(payloads) == 1 else f".{idx}"
            target = out_dir / f"{Path(name).name}{suffix}"
            target.write_bytes(data)
            written.append(str(target))
    return {"operation": "extract-attachments", "input": str(args.input), "output_dir": str(out_dir), "files": written}


def cmd_reduce(args) -> dict[str, Any]:
    reader = reader_for(args.input, args.password)
    writer = PdfWriter()
    for page in reader.pages:
        if args.compress_streams:
            try:
                page.compress_content_streams()
            except Exception:
                pass
        writer.add_page(page)
    copy_metadata(reader, writer)
    try:
        writer.compress_identical_objects()
    except Exception:
        pass
    out = resolve_output(args.output, force=args.force)
    return write_pdf(
        writer,
        out,
        manifest={"operation": "reduce", "input": str(args.input), "compress_streams": args.compress_streams},
        no_manifest=args.no_manifest,
    )


def add_common_io(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--force", action="store_true", help="Allow overwriting output")
    parser.add_argument("--no-manifest", action="store_true", help="Do not write output manifest JSON")


def add_password(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--password", help="Input PDF password")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local PDF surgery and assembly with pypdf.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("self-check")
    p.set_defaults(func=cmd_self_check)

    p = sub.add_parser("info")
    p.add_argument("input")
    add_password(p)
    p.set_defaults(func=cmd_info)

    p = sub.add_parser("extract")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("pages")
    add_password(p)
    add_common_io(p)
    p.set_defaults(func=cmd_extract)

    p = sub.add_parser("delete")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("pages")
    add_password(p)
    add_common_io(p)
    p.set_defaults(func=cmd_delete)

    p = sub.add_parser("merge")
    p.add_argument("output")
    p.add_argument("inputs", nargs="+")
    p.add_argument("--no-outlines", action="store_true", help="Do not import outlines/bookmarks")
    add_common_io(p)
    p.set_defaults(func=cmd_merge)

    p = sub.add_parser("replace")
    p.add_argument("source")
    p.add_argument("replacement")
    p.add_argument("output")
    p.add_argument("pages")
    add_password(p)
    p.add_argument("--replacement-password")
    add_common_io(p)
    p.set_defaults(func=cmd_replace)

    p = sub.add_parser("insert")
    p.add_argument("source")
    p.add_argument("insert")
    p.add_argument("output")
    p.add_argument("--before", type=int)
    p.add_argument("--after", type=int)
    add_password(p)
    p.add_argument("--insert-password")
    add_common_io(p)
    p.set_defaults(func=cmd_insert)

    p = sub.add_parser("rotate")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("degrees", type=int)
    p.add_argument("--pages", default="all")
    add_password(p)
    add_common_io(p)
    p.set_defaults(func=cmd_rotate)

    p = sub.add_parser("crop")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--pages", default="all")
    p.add_argument("--left", type=float, default=0)
    p.add_argument("--bottom", type=float, default=0)
    p.add_argument("--right", type=float, default=0)
    p.add_argument("--top", type=float, default=0)
    add_password(p)
    add_common_io(p)
    p.set_defaults(func=cmd_crop)

    p = sub.add_parser("stamp")
    p.add_argument("input")
    p.add_argument("stamp")
    p.add_argument("output")
    p.add_argument("--pages", default="all")
    p.add_argument("--mode", choices=["over", "under"], default="over")
    add_password(p)
    p.add_argument("--stamp-password")
    add_common_io(p)
    p.set_defaults(func=cmd_stamp)

    p = sub.add_parser("encrypt")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--password", help="Existing input PDF password, if encrypted")
    p.add_argument("--new-password", required=True, help="New user password")
    p.add_argument("--owner-password")
    p.add_argument("--algorithm", default="AES-256-R5", choices=["RC4-40", "RC4-128", "AES-128", "AES-256-R5", "AES-256"])
    add_common_io(p)
    p.set_defaults(func=cmd_encrypt)

    p = sub.add_parser("decrypt")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--password", required=True)
    add_common_io(p)
    p.set_defaults(func=cmd_decrypt)

    p = sub.add_parser("metadata")
    p.add_argument("input")
    add_password(p)
    p.set_defaults(func=cmd_metadata)

    p = sub.add_parser("set-metadata")
    p.add_argument("input")
    p.add_argument("output")
    for attr in METADATA_FLAGS:
        p.add_argument(f"--{attr}")
    p.add_argument("--clear", action="store_true", help="Clear old metadata before adding provided values")
    add_password(p)
    add_common_io(p)
    p.set_defaults(func=cmd_set_metadata)

    p = sub.add_parser("list-fields")
    p.add_argument("input")
    add_password(p)
    p.set_defaults(func=cmd_list_fields)

    p = sub.add_parser("fill-form")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("fields_json")
    p.add_argument("--all-pages", action="store_true")
    p.add_argument("--flatten", action="store_true")
    add_password(p)
    add_common_io(p)
    p.set_defaults(func=cmd_fill_form)

    p = sub.add_parser("attach")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("files", nargs="+")
    add_password(p)
    add_common_io(p)
    p.set_defaults(func=cmd_attach)

    p = sub.add_parser("extract-attachments")
    p.add_argument("input")
    p.add_argument("output_dir")
    add_password(p)
    p.set_defaults(func=cmd_extract_attachments)

    p = sub.add_parser("reduce")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--no-compress-streams", dest="compress_streams", action="store_false")
    p.set_defaults(compress_streams=True)
    add_password(p)
    add_common_io(p)
    p.set_defaults(func=cmd_reduce)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
