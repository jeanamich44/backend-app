from functools import lru_cache
from pathlib import Path
from PIL import Image
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from app.services.generate_docs.common.paths import LOGOS_DIR
from . import layout

# ----------------------------------------------------------------------

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

# ----------------------------------------------------------------------

def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top

# ----------------------------------------------------------------------

def to_color(color):
    if isinstance(color, Color):
        return color
    if isinstance(color, str):
        return HexColor(color)
    r, g, b = color[0], color[1], color[2]
    alpha = color[3] if len(color) > 3 else 1
    return Color(r, g, b, alpha=alpha)

# ----------------------------------------------------------------------

def char_space_for(size: float) -> float:
    if abs(size - layout.SIZE_TEXT_SM) < 0.05:
        return layout.CHAR_SPACE_SM
    if abs(size - layout.SIZE_TEXT_MD) < 0.05:
        return layout.CHAR_SPACE_MD
    if abs(size - layout.SIZE_TEXT_LG) < 0.05:
        return layout.CHAR_SPACE_LG
    if abs(size - layout.SIZE_TEXT_XL) < 0.05:
        return layout.CHAR_SPACE_XL
    return 0.0

# ----------------------------------------------------------------------

def width(text: str, font: str, size: float, char_space: float | None = None) -> float:
    text = text or ""
    cs = char_space_for(size) if char_space is None else char_space
    w = stringWidth(text, font, size)
    if cs and len(text) > 1:
        w += (len(text) - 1) * cs
    return w

# ----------------------------------------------------------------------

def clip(text: str, font: str, size: float, max_width: float | None, char_space: float | None = None) -> str:
    text = text or ""
    if max_width is None or width(text, font, size, char_space=char_space) <= max_width:
        return text
    while text and width(text, font, size, char_space=char_space) > max_width:
        text = text[:-1]
    return text

# ----------------------------------------------------------------------

def draw_string(c, x: float, y_origin: float, text: str, font: str, size: float, color=layout.COLOR_TEXT, max_width=None, char_space=None, bold=False):
    cs = char_space_for(size) if char_space is None else char_space
    text = clip(text, font, size, max_width, char_space=cs)
    if not text:
        return
    c.saveState()
    c.setFillColor(to_color(color))
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text, charSpace=cs)
    if bold:
        c.drawString(x + layout.BOLD_DX, y_up(y_origin), text, charSpace=cs)
    c.restoreState()

# ----------------------------------------------------------------------

def draw_right(c, x: float, y_origin: float, text: str, font: str, size: float, color=layout.COLOR_TEXT, max_width=None, char_space=None, bold=False):
    cs = char_space_for(size) if char_space is None else char_space
    text = clip(text, font, size, max_width, char_space=cs)
    if not text:
        return
    c.saveState()
    c.setFillColor(to_color(color))
    c.setFont(font, size)
    c.drawRightString(x, y_up(y_origin), text, charSpace=cs)
    if bold:
        c.drawRightString(x + layout.BOLD_DX, y_up(y_origin), text, charSpace=cs)
    c.restoreState()

# ----------------------------------------------------------------------

def draw_center(c, x: float, y_origin: float, text: str, font: str, size: float, color=layout.COLOR_TEXT, max_width=None, char_space=None, bold=False):
    cs = char_space_for(size) if char_space is None else char_space
    text = clip(text, font, size, max_width, char_space=cs)
    if not text:
        return
    c.saveState()
    c.setFillColor(to_color(color))
    c.setFont(font, size)
    c.drawCentredString(x, y_up(y_origin), text, charSpace=cs)
    if bold:
        c.drawCentredString(x + layout.BOLD_DX, y_up(y_origin), text, charSpace=cs)
    c.restoreState()

# ----------------------------------------------------------------------

def fill_rect(c, x0: float, y0: float, x1: float, y1: float, color):
    c.saveState()
    c.setFillColor(to_color(color))
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=0, fill=1)
    c.restoreState()

# ----------------------------------------------------------------------

def stroke_line(c, x0: float, y0: float, x1: float, y1: float, line_w: float, color, cap: int = 0):
    c.saveState()
    c.setStrokeColor(to_color(color))
    c.setLineWidth(line_w)
    c.setLineCap(cap)
    c.setLineJoin(0)
    c.setDash([], 0)
    c.line(x0, y_up(y0), x1, y_up(y1))
    c.restoreState()

# ----------------------------------------------------------------------

def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float):
    c.saveState()
    path = str(LOGOS_DIR / filename)
    c.drawImage(
        _image(path),
        x, y_up(y_top + h),
        width=w, height=h, mask="auto",
        preserveAspectRatio=False, anchor="c",
    )
    c.restoreState()
