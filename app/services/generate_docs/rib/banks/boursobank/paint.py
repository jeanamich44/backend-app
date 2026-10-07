"""Helpers dessin (Y ReportLab, PNG, clip)."""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

from app.services.generate_docs.common.paths import LOGOS_DIR

from . import layout

CHROME_DIR = Path(__file__).resolve().parent / "chrome"


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


def fill(c, hex_color: str):
    c.setFillColor(HexColor(hex_color))


def clip(text, font, size, max_width):
    text = text or ""
    if max_width is None or stringWidth(text, font, size) <= max_width:
        return text
    while text and stringWidth(text, font, size) > max_width:
        text = text[:-1]
    return text


def draw_string(c, x: float, y_origin: float, text: str, font: str, size: float, max_width=None):
    text = clip(text, font, size, max_width)
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text)


def draw_right(c, x: float, y_origin: float, text: str, font: str, size: float, max_width=None):
    text = clip(text, font, size, max_width)
    c.setFont(font, size)
    c.drawRightString(x, y_up(y_origin), text)


def _png(c, path: Path, x: float, y_top: float, w: float, h: float):
    c.drawImage(str(path), x, y_up(y_top + h), width=w, height=h, mask="auto")


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float):
    _png(c, LOGOS_DIR / filename, x, y_top, w, h)


def draw_chrome(c, filename: str, x: float, y_top: float, w: float, h: float):
    _png(c, CHROME_DIR / filename, x, y_top, w, h)
