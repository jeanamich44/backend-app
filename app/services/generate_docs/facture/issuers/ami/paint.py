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


def draw_right(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    c.setFont(font, size)
    c.drawRightString(x, y_up(y_origin), text)


def fill_rect(c, x0: float, y0: float, x1: float, y1: float, color):
    c.saveState()
    c.setFillColor(to_color(color))
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=0, fill=1)
    c.restoreState()


def fill_subpaths(c, subpaths, color, dy: float = 0.0):
    """Rejoue un fill du blueprint : U ouverts, winding nonzero (`f`, pas `f*`)."""
    c.saveState()
    c.setFillColor(to_color(color))
    path = c.beginPath()
    for pts in subpaths:
        if len(pts) < 2:
            continue
        x0, y0 = pts[0]
        path.moveTo(x0, y_up(y0 + dy))
        for x, y in pts[1:]:
            path.lineTo(x, y_up(y + dy))
    c.drawPath(path, stroke=0, fill=1, fillMode=FILL_NON_ZERO)
    c.restoreState()


def extend_down(subpaths, extra: float):
    """Garde le tracé 1 ligne, ajoute des U sous le dernier pour N>1."""
    if extra <= 0 or not subpaths:
        return subpaths
    bottoms = [max(p[1] for p in sp) for sp in subpaths]
    y0 = max(bottoms)
    uniq = sorted(set(round(b, 2) for b in bottoms), reverse=True)
    period = uniq[0] - uniq[1] if len(uniq) > 1 else 1.5
    template = max(subpaths, key=lambda sp: max(p[1] for p in sp))
    ty = max(p[1] for p in template)
    out = list(subpaths)
    y = y0 + period
    limit = y0 + extra
    while y <= limit + 0.02:
        shift = y - ty
        out.append(tuple((x, yy + shift) for x, yy in template))
        y += period
    return tuple(out)


def stroke_line(
    c, x0: float, y0: float, x1: float, y1: float,
    line_w: float, color, cap: int = 0,
):
    c.saveState()
    c.setStrokeColor(to_color(color))
    c.setLineWidth(line_w)
    c.setLineCap(cap)
    c.setLineJoin(0)
    c.setDash([], 0)
    c.line(x0, y_up(y0), x1, y_up(y1))
    c.restoreState()


def clip_rect(c, x: float, y_top: float, w: float, h: float):
    path = c.beginPath()
    path.rect(x, y_up(y_top + h), w, h)
    c.clipPath(path, stroke=0, fill=0)


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
