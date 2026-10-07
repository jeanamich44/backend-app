"""Helpers dessin (Y ReportLab, fill, images chrome)."""

from functools import lru_cache
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

from app.services.generate_docs.common.paths import LOGOS_DIR

from . import layout

CHROME_DIR = Path(__file__).resolve().parent / "chrome"


@lru_cache(maxsize=16)
def _image(path: str) -> ImageReader:
    """Garde le RGB d'origine + SMask. convert('RGB') sur RGBA composite sur noir."""
    im = Image.open(path)
    if im.mode == "RGBA":
        red, green, blue, alpha = im.split()
        reader = ImageReader(Image.merge("RGB", (red, green, blue)))
        reader.getRGBData()
        reader._dataA = ImageReader(alpha)
        return reader
    return ImageReader(im)


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


def fill(c, hex_color: str):
    c.setFillColor(HexColor(hex_color))


def width(text, font, size) -> float:
    return stringWidth(text or "", font, size)


def clip(text, font, size, max_width):
    text = text or ""
    if max_width is None or width(text, font, size) <= max_width:
        return text
    while text and width(text, font, size) > max_width:
        text = text[:-1]
    return text


def draw_string(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text)


def draw_runs(c, x: float, y_origin: float, runs) -> float:
    cursor = x
    for text, font, size in runs:
        if not text:
            continue
        c.setFont(font, size)
        c.drawString(cursor, y_up(y_origin), text)
        cursor += width(text, font, size)
    return cursor


def fill_rect(c, x0: float, y0: float, x1: float, y1: float, hex_color: str):
    c.saveState()
    c.setFillColor(HexColor(hex_color))
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=0, fill=1)
    c.restoreState()


def stroke_line(c, x0: float, y: float, x1: float, line_w: float, hex_color: str):
    c.saveState()
    c.setStrokeColor(HexColor(hex_color))
    c.setLineWidth(line_w)
    c.setLineCap(0)
    yu = y_up(y)
    c.line(x0, yu, x1, yu)
    c.restoreState()


def round_rect(
    c, x0: float, y0: float, x1: float, y1: float, radius: float,
    fill_hex: str, stroke_hex: str, stroke_w: float,
):
    w, h = x1 - x0, y1 - y0
    c.saveState()
    c.setFillColor(HexColor(fill_hex))
    c.setStrokeColor(HexColor(stroke_hex))
    c.setLineWidth(stroke_w)
    c.roundRect(x0, y_up(y1), w, h, radius, stroke=1, fill=1)
    c.restoreState()


def _draw_png(c, path: Path, x: float, y_top: float, w: float, h: float):
    c.saveState()
    c.drawImage(
        _image(str(path)),
        x, y_up(y_top + h),
        width=w, height=h, mask="auto",
        preserveAspectRatio=False, anchor="c",
    )
    c.restoreState()


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float):
    _draw_png(c, LOGOS_DIR / filename, x, y_top, w, h)


def draw_chrome(c, filename: str, x: float, y_top: float, w: float, h: float):
    _draw_png(c, CHROME_DIR / filename, x, y_top, w, h)


def badge(c, x0: float, y0: float, number: str):
    fill_rect(c, x0, y0, x0 + layout.BADGE_W, y0 + layout.BADGE_H, layout.COLOR_BADGE)
    fill(c, layout.COLOR_WHITE)
    draw_string(
        c,
        x0 + layout.BADGE_NUM_DX,
        y0 + layout.BADGE_NUM_DY,
        number,
        layout.FONT_BOLD,
        layout.SIZE_BADGE,
    )
