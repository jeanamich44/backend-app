"""Helpers dessin (Y ReportLab, fill, images)."""

from functools import lru_cache

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

from app.services.generate_docs.common.paths import LOGOS_DIR

from . import layout


@lru_cache(maxsize=16)
def _image(path: str) -> ImageReader:
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


def _stroke_setup(c, line_w: float, hex_color: str, cap: int, dash):
    c.setStrokeColor(HexColor(hex_color))
    c.setLineWidth(line_w)
    c.setLineCap(cap)
    c.setLineJoin(0)
    if dash:
        c.setDash(list(dash), 0)
    else:
        c.setDash([], 0)


def stroke_line(
    c, x0: float, y0: float, x1: float, y1: float,
    line_w: float, hex_color: str, cap: int = 0, dash=None,
):
    c.saveState()
    _stroke_setup(c, line_w, hex_color, cap, dash)
    c.line(x0, y_up(y0), x1, y_up(y1))
    c.restoreState()


def stroke_u(c, x0: float, x1: float, y_top: float, y_bot: float, line_w: float, hex_color: str):
    """3 segments (bas, gauche, haut), cap carré — en-tête du gabarit."""
    c.saveState()
    _stroke_setup(c, line_w, hex_color, 2, None)
    p = c.beginPath()
    p.moveTo(x1, y_up(y_bot))
    p.lineTo(x0, y_up(y_bot))
    p.lineTo(x0, y_up(y_top))
    p.lineTo(x1, y_up(y_top))
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def stroke_re(c, x0: float, y0: float, x1: float, y1: float, line_w: float, hex_color: str):
    c.saveState()
    _stroke_setup(c, line_w, hex_color, 0, None)
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=1, fill=0)
    c.restoreState()


def stroke_path(c, ops, line_w: float, hex_color: str, cap: int = 0):
    c.saveState()
    _stroke_setup(c, line_w, hex_color, cap, None)
    p = c.beginPath()
    for op in ops:
        kind = op[0]
        if kind == "m":
            p.moveTo(op[1], y_up(op[2]))
        elif kind == "l":
            p.lineTo(op[1], y_up(op[2]))
        elif kind == "c":
            p.curveTo(
                op[1], y_up(op[2]),
                op[3], y_up(op[4]),
                op[5], y_up(op[6]),
            )
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float):
    c.saveState()
    c.drawImage(
        _image(str(LOGOS_DIR / filename)),
        x, y_up(y_top + h),
        width=w, height=h, mask="auto",
        preserveAspectRatio=False, anchor="c",
    )
    c.restoreState()
