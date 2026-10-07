"""Helpers dessin (Y ReportLab depuis le haut PyMuPDF)."""

from functools import lru_cache
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import FILL_NON_ZERO

from app.services.generate_docs.common.paths import LOGOS_DIR

from . import layout

CHROME_DIR = Path(__file__).resolve().parent / "chrome"


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


def to_color(color):
    if isinstance(color, Color):
        return color
    if isinstance(color, str):
        return HexColor(color)
    r, g, b = color[0], color[1], color[2]
    alpha = color[3] if len(color) > 3 else 1
    return Color(r, g, b, alpha=alpha)


def fill(c, color):
    c.setFillColor(to_color(color))


def width(text, font, size, char_space=0) -> float:
    text = text or ""
    extra = char_space * (len(text) - 1) if len(text) > 1 else 0
    return stringWidth(text, font, size) + extra


def clip(text, font, size, max_width, char_space=0):
    text = text or ""
    if max_width is None or width(text, font, size, char_space) <= max_width:
        return text
    while text and width(text, font, size, char_space) > max_width:
        text = text[:-1]
    return text


def draw_string(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None, char_space=0,
):
    text = clip(text, font, size, max_width, char_space)
    if not text:
        return
    c.saveState()
    t = c.beginText()
    t.setFont(font, size)
    t.setCharSpace(char_space)
    t.setTextOrigin(x, y_up(y_origin))
    t.textOut(text)
    c.drawText(t)
    c.restoreState()


def draw_glyphs(c, y_origin: float, glyphs, font: str, size: float):
    """Une origine X par glyphe (crénage TJ du gabarit)."""
    if not glyphs:
        return
    c.saveState()
    t = c.beginText()
    t.setFont(font, size)
    t.setCharSpace(0)
    y = y_up(y_origin)
    for ch, x in glyphs:
        if ch:
            t.setTextOrigin(x, y)
            t.textOut(ch)
    c.drawText(t)
    c.restoreState()


def draw_right(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    c.setFont(font, size)
    c.drawRightString(x, y_up(y_origin), text)


def draw_string_rot90(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    char_space=0,
):
    if not text:
        return
    c.saveState()
    c.translate(x, y_up(y_origin))
    c.rotate(90)
    t = c.beginText()
    t.setFont(font, size)
    t.setCharSpace(char_space)
    t.setTextOrigin(0, 0)
    t.textOut(text)
    c.drawText(t)
    c.restoreState()


def fill_rect(c, x0: float, y0: float, x1: float, y1: float, color):
    c.saveState()
    c.setFillColor(to_color(color))
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=0, fill=1)
    c.restoreState()


def _path_from_ops(c, ops):
    path = c.beginPath()
    started = False
    cur = None
    for op in ops:
        kind = op[0]
        if kind == "re":
            x0, y0, x1, y1 = op[1], op[2], op[3], op[4]
            top, bot = min(y0, y1), max(y0, y1)
            left, right = min(x0, x1), max(x0, x1)
            path.rect(left, y_up(bot), right - left, bot - top)
            started = False
            cur = None
        elif kind == "m":
            path.moveTo(op[1], y_up(op[2]))
            cur = (op[1], op[2])
            started = True
        elif kind == "l":
            x0, y0, x1, y1 = op[1], op[2], op[3], op[4]
            if not started or cur is None or abs(cur[0] - x0) > 0.02 or abs(cur[1] - y0) > 0.02:
                path.moveTo(x0, y_up(y0))
            path.lineTo(x1, y_up(y1))
            cur = (x1, y1)
            started = True
        elif kind == "c":
            x0, y0, x1, y1, x2, y2, x3, y3 = op[1:9]
            if not started or cur is None or abs(cur[0] - x0) > 0.02 or abs(cur[1] - y0) > 0.02:
                path.moveTo(x0, y_up(y0))
            path.curveTo(x1, y_up(y1), x2, y_up(y2), x3, y_up(y3))
            cur = (x3, y3)
            started = True
    return path


def fill_ops(c, ops, color):
    c.saveState()
    c.setFillColor(to_color(color))
    c.drawPath(_path_from_ops(c, ops), stroke=0, fill=1, fillMode=FILL_NON_ZERO)
    c.restoreState()


def stroke_ops(c, ops, color, width, cap=0):
    c.saveState()
    c.setStrokeColor(to_color(color))
    c.setFillColor(to_color(color))
    c.setLineWidth(width)
    c.setLineCap(cap)
    c.setLineJoin(0)
    c.setDash([], 0)
    c.drawPath(_path_from_ops(c, ops), stroke=1, fill=0)
    c.restoreState()


def wrap_lines(text, font, size, max_width):
    words = (text or "").split()
    if not words:
        return []
    lines, cur = [], words[0]
    for word in words[1:]:
        trial = f"{cur} {word}"
        if width(trial, font, size) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


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
