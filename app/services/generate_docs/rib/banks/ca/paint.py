"""Helpers dessin (Y ReportLab, crénage gabarit, logo, filets, clip)."""

import json
from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from svglib.svglib import svg2rlg

from app.services.generate_docs.common.paths import LOGOS_DIR

from . import layout

_UPEM = 2048.0
_KERN = json.loads(
    (Path(__file__).resolve().parent / "chrome" / "kern.json").read_text(encoding="utf-8")
)
_svg = {}


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


def fill(c, hex_color: str):
    c.setFillColor(HexColor(hex_color))


def _kern_pt(font: str, a: str, b: str, size: float) -> float:
    units = _KERN.get(font, {}).get(a, {}).get(b)
    if not units:
        return 0.0
    return units * size / _UPEM


def width(text, font, size) -> float:
    text = text or ""
    total = 0.0
    for i, ch in enumerate(text):
        total += stringWidth(ch, font, size)
        if i + 1 < len(text):
            total += _kern_pt(font, ch, text[i + 1], size)
    return total


def clip(text, font, size, max_width):
    text = text or ""
    if max_width is None or width(text, font, size) <= max_width:
        return text
    while text and width(text, font, size) > max_width:
        text = text[:-1]
    return text


def draw_string(c, x: float, y_origin: float, text: str, font: str, size: float, max_width=None):
    text = clip(text, font, size, max_width)
    if not text:
        return
    y = y_up(y_origin)
    c.setFont(font, size)
    cursor = x
    n = len(text)
    for i, ch in enumerate(text):
        c.drawString(cursor, y, ch)
        cursor += stringWidth(ch, font, size)
        if i + 1 < n:
            cursor += _kern_pt(font, ch, text[i + 1], size)


def draw_right(c, x: float, y_origin: float, text: str, font: str, size: float, max_width=None):
    text = clip(text, font, size, max_width)
    if not text:
        return
    draw_string(c, x - width(text, font, size), y_origin, text, font, size)


def fill_rect(c, x0, y0, x1, y1, hex_color: str):
    c.saveState()
    c.setFillColor(HexColor(hex_color))
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=0, fill=1)
    c.restoreState()


def wrap_lines(text: str, font: str, size: float, max_width: float) -> list[str]:
    lines = []
    current = ""
    for word in (text or "").split():
        trial = word if not current else f"{current} {word}"
        if width(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def _load_svg(path: Path):
    key = str(path)
    if key not in _svg:
        loaded = svg2rlg(str(path))
        if loaded is None:
            raise FileNotFoundError(f"SVG introuvable : {path}")
        _svg[key] = loaded
    return _svg[key]


def draw_svg(c, filename: str, x: float, y_top: float, w: float, h: float, dx: float = 0.0):
    path = LOGOS_DIR / filename
    drawing = _load_svg(path)
    if not drawing.width or not drawing.height:
        return
    c.saveState()
    c.translate(x + dx, y_up(y_top + h))
    c.scale(w / drawing.width, h / drawing.height)
    renderPDF.draw(drawing, c, 0, 0, showBoundary=0)
    c.restoreState()
