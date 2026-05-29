from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Literal, Optional


SKILL_DIR = Path(__file__).resolve().parents[1]
LOCAL_SITE = SKILL_DIR / "tools" / "python"
if LOCAL_SITE.exists():
    sys.path.insert(0, str(LOCAL_SITE))

try:
    import qrcode
    from qrcode.image.svg import SvgPathImage
except ImportError as exc:
    qrcode = None
    SvgPathImage = None
    QR_IMPORT_ERROR = exc
else:
    QR_IMPORT_ERROR = None

try:
    from PIL import Image, ImageColor
except ImportError as exc:
    Image = None
    ImageColor = None
    PIL_IMPORT_ERROR = exc
else:
    PIL_IMPORT_ERROR = None


ErrorLevel = Literal["L", "M", "Q", "H"]
OutputFormat = Literal["png", "svg"]


ERROR_MAP = {
    "L": "ERROR_CORRECT_L",
    "M": "ERROR_CORRECT_M",
    "Q": "ERROR_CORRECT_Q",
    "H": "ERROR_CORRECT_H",
}


def _require_deps() -> None:
    missing = []
    if QR_IMPORT_ERROR is not None:
        missing.append("qrcode")
    if PIL_IMPORT_ERROR is not None:
        missing.append("Pillow")
    if missing:
        install = (
            f'python -m pip install --target "{LOCAL_SITE}" "qrcode[pil]"'
        )
        raise RuntimeError(
            "Missing Python package(s): "
            + ", ".join(missing)
            + ". Install locally with: "
            + install
        )


def _error_constant(level: ErrorLevel) -> int:
    _require_deps()
    if level not in ERROR_MAP:
        raise ValueError("error_level must be one of: L, M, Q, H")
    return getattr(qrcode.constants, ERROR_MAP[level])


def normalize_payload(data: str, *, assume_url: bool = True) -> str:
    payload = (data or "").strip()
    if not payload:
        raise ValueError("data cannot be empty")
    if assume_url and _looks_like_domain(payload) and not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", payload):
        return "https://" + payload
    return payload


def _looks_like_domain(value: str) -> bool:
    if any(ch.isspace() for ch in value):
        return False
    if "@" in value:
        return False
    return bool(re.match(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:[/:?#].*)?$", value))


def _resolve_output_path(output_path: str, output_format: OutputFormat) -> Path:
    path = Path(output_path)
    if not path.is_absolute():
        path = Path.cwd() / path
    suffix = "." + output_format
    if path.suffix.lower() != suffix:
        path = path.with_suffix(suffix)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _rgb(color: str) -> tuple[int, int, int]:
    _require_deps()
    return ImageColor.getrgb(color)[:3]


def _relative_luminance(color: tuple[int, int, int]) -> float:
    def channel(c: int) -> float:
        v = c / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in color)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: str, b: str) -> float:
    la = _relative_luminance(_rgb(a))
    lb = _relative_luminance(_rgb(b))
    lighter = max(la, lb)
    darker = min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def _lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


def _gradient_color(start: tuple[int, int, int], end: tuple[int, int, int], x: int, y: int, max_x: int, max_y: int) -> tuple[int, int, int]:
    denom = max(1, max_x + max_y)
    t = (x + y) / denom
    return (_lerp(start[0], end[0], t), _lerp(start[1], end[1], t), _lerp(start[2], end[2], t))


def _build_qr(data: str, error_level: ErrorLevel, box_size: int, border: int):
    _require_deps()
    if box_size < 1:
        raise ValueError("box_size must be >= 1")
    if border < 4:
        raise ValueError("border should stay >= 4 for reliable scanning")
    qr = qrcode.QRCode(
        version=None,
        error_correction=_error_constant(error_level),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr


def _make_gradient_png(qr, box_size: int, border: int, back_color: str, gradient: tuple[str, str]):
    _require_deps()
    matrix = qr.get_matrix()
    modules = len(matrix)
    size = modules * box_size
    image = Image.new("RGB", (size, size), _rgb(back_color))
    start = _rgb(gradient[0])
    end = _rgb(gradient[1])
    max_index = modules - 1

    for y, row in enumerate(matrix):
        for x, dark in enumerate(row):
            if not dark:
                continue
            color = _gradient_color(start, end, x, y, max_index, max_index)
            left = x * box_size
            top = y * box_size
            image.paste(color, (left, top, left + box_size, top + box_size))
    return image


def generate_qr(
    data: str,
    output_path: str = "qr.png",
    *,
    error_level: ErrorLevel = "H",
    box_size: int = 16,
    border: int = 4,
    fill_color: str = "black",
    back_color: str = "white",
    output_format: Optional[OutputFormat] = None,
    gradient: Optional[tuple[str, str]] = None,
    assume_url: bool = True,
) -> str:
    payload = normalize_payload(data, assume_url=assume_url)
    fmt = output_format or ("svg" if Path(output_path).suffix.lower() == ".svg" else "png")
    if fmt not in ("png", "svg"):
        raise ValueError("output_format must be png or svg")

    path = _resolve_output_path(output_path, fmt)
    qr = _build_qr(payload, error_level, box_size, border)

    if fmt == "svg":
        if gradient:
            raise ValueError("gradient output is supported for PNG only")
        img = qr.make_image(image_factory=SvgPathImage, fill_color=fill_color, back_color=back_color)
        img.save(path)
    else:
        if gradient:
            img = _make_gradient_png(qr, box_size, border, back_color, gradient)
        else:
            img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")
        img.save(path)

    return str(path)


def _warn_scan_risks(args) -> list[str]:
    warnings = []
    if args.border < 4:
        warnings.append("border below 4 modules can reduce scan reliability")
    if args.gradient and args.error_level != "H":
        warnings.append("styled or gradient QR codes should usually use error level H")
    try:
        if args.gradient:
            ratios = [contrast_ratio(args.gradient[0], args.back), contrast_ratio(args.gradient[1], args.back)]
            if min(ratios) < 3:
                warnings.append(f"low foreground/background contrast detected: min ratio {min(ratios):.2f}")
        else:
            ratio = contrast_ratio(args.fill, args.back)
            if ratio < 3:
                warnings.append(f"low foreground/background contrast detected: ratio {ratio:.2f}")
    except Exception as exc:
        warnings.append(f"could not evaluate color contrast: {exc}")
    return warnings


def _png_size(path: Path) -> str:
    if Image is None or path.suffix.lower() != ".png":
        return ""
    with Image.open(path) as img:
        return f"{img.width}x{img.height}px"


def _run_one(args) -> dict:
    out = generate_qr(
        data=args.data,
        output_path=args.output,
        error_level=args.error_level,
        box_size=args.box_size,
        border=args.border,
        fill_color=args.fill,
        back_color=args.back,
        output_format=args.format,
        gradient=tuple(args.gradient) if args.gradient else None,
        assume_url=not args.no_assume_url,
    )
    path = Path(out)
    return {
        "path": str(path),
        "format": path.suffix.lower().lstrip("."),
        "error_level": args.error_level,
        "size": _png_size(path),
        "warnings": _warn_scan_risks(args),
    }


def _run_batch(batch_path: str) -> list[dict]:
    src = Path(batch_path)
    items = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(items, list):
        raise ValueError("batch file must contain a JSON array")
    results = []
    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"batch item {idx} must be an object")
        gradient = item.get("gradient")
        if gradient is not None:
            gradient = tuple(gradient)
        out = generate_qr(
            data=item["data"],
            output_path=item.get("output_path", f"qr-{idx:03d}.png"),
            error_level=item.get("error_level", "H"),
            box_size=int(item.get("box_size", 16)),
            border=int(item.get("border", 4)),
            fill_color=item.get("fill_color", "black"),
            back_color=item.get("back_color", "white"),
            output_format=item.get("output_format"),
            gradient=gradient,
            assume_url=bool(item.get("assume_url", True)),
        )
        results.append({"path": out})
    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate scan-safe QR codes in the current directory.")
    parser.add_argument("data", nargs="?", help="URL or arbitrary text payload")
    parser.add_argument("--output", "-o", default="qr.png", help="Output path, relative to current directory by default")
    parser.add_argument("--format", choices=["png", "svg"], help="Output format; inferred from extension when omitted")
    parser.add_argument("--error-level", choices=["L", "M", "Q", "H"], default="H", help="QR error correction level")
    parser.add_argument("--box-size", type=int, default=16, help="Pixel size of one QR module")
    parser.add_argument("--border", type=int, default=4, help="Quiet-zone border in QR modules")
    parser.add_argument("--fill", default="black", help="Foreground color for solid QR modules")
    parser.add_argument("--back", default="white", help="Background color")
    parser.add_argument("--gradient", nargs=2, metavar=("START", "END"), help="PNG-only module gradient from START to END color")
    parser.add_argument("--no-assume-url", action="store_true", help="Do not add https:// to domain-like payloads")
    parser.add_argument("--batch", help="Path to JSON array with QR generation jobs")
    parser.add_argument("--self-check", action="store_true", help="Check local dependencies and exit")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_check:
        try:
            _require_deps()
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            return 2
        print("OK: qrcode and Pillow are available")
        return 0

    try:
        if args.batch:
            results = _run_batch(args.batch)
        else:
            if not args.data:
                parser.error("data is required unless --batch or --self-check is used")
            results = [_run_one(args)]
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
