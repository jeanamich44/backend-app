from PIL import Image
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.utils import ImageReader
from app.services.generate_docs.common.paths import LOGOS_DIR
from . import layout

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

def draw_text(c, x: float, y_origin: float, text: str, font: str, size: float, color=layout.COLOR_BLACK, char_space: float = 0.0):
    if not text:
        return
    c.saveState()
    c.setFillColor(to_color(color))
    c.setFont(font, size)
    tx = c.beginPath()
    c.setStrokeColor(to_color(color))
    text_obj = c.beginText(x, y_up(y_origin))
    text_obj.setFont(font, size)
    text_obj.setFillColor(to_color(color))
    if char_space != 0.0:
        text_obj.setCharSpace(char_space)
    text_obj.textOut(text)
    c.drawText(text_obj)
    c.restoreState()

# ----------------------------------------------------------------------

def draw_line(c, x1: float, y1: float, x2: float, y2: float, width: float = 1.0, color=layout.COLOR_GREY):
    c.saveState()
    c.setStrokeColor(to_color(color))
    c.setLineWidth(width)
    c.setLineCap(0)
    c.line(x1, y_up(y1), x2, y_up(y2))
    c.restoreState()

# ----------------------------------------------------------------------

def draw_rect(c, x: float, y_top: float, w: float, h: float, fill_color=None, stroke_color=None, stroke_width: float = 1.0):
    c.saveState()
    do_fill = 0
    do_stroke = 0
    if fill_color is not None:
        c.setFillColor(to_color(fill_color))
        do_fill = 1
    if stroke_color is not None:
        c.setStrokeColor(to_color(stroke_color))
        c.setLineWidth(stroke_width)
        c.setLineCap(0)
        c.setLineJoin(0)
        do_stroke = 1
    c.rect(x, y_up(y_top + h), w, h, stroke=do_stroke, fill=do_fill)
    c.restoreState()

# ----------------------------------------------------------------------

def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float):
    path = LOGOS_DIR / filename
    im = Image.open(str(path))
    if im.mode == "RGBA":
        red, green, blue, alpha = im.split()
        reader = ImageReader(Image.merge("RGB", (red, green, blue)))
        reader.getRGBData()
        reader._dataA = ImageReader(alpha)
    else:
        reader = ImageReader(im)
    c.saveState()
    c.drawImage(reader, x, y_up(y_top + h), width=w, height=h, mask="auto")
    c.restoreState()
