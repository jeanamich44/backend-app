from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from . import layout

CHROME_DIR = Path(__file__).resolve().parent / "chrome"

# ----------------------------------------------------------------------

def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top

# ----------------------------------------------------------------------

def fill(c, hex_color: str):
    c.setFillColor(HexColor(hex_color))

# ----------------------------------------------------------------------

def stroke(c, hex_color: str):
    c.setStrokeColor(HexColor(hex_color))

# ----------------------------------------------------------------------

def clip(text, font, size, max_width):
    text = text or ""
    if max_width is None or stringWidth(text, font, size) <= max_width:
        return text
    while text and stringWidth(text, font, size) > max_width:
        text = text[:-1]
    return text

# ----------------------------------------------------------------------

def draw_string(c, x: float, y_origin: float, text: str, font: str, size: float, max_width=None):
    text = clip(text, font, size, max_width)
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text)

# ----------------------------------------------------------------------

def draw_right(c, x: float, y_origin: float, text: str, font: str, size: float, max_width=None):
    text = clip(text, font, size, max_width)
    c.setFont(font, size)
    c.drawRightString(x, y_up(y_origin), text)

# ----------------------------------------------------------------------

def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float):
    path = CHROME_DIR / filename
    c.drawImage(str(path), x, y_up(y_top + h), width=w, height=h, mask="auto")

# ----------------------------------------------------------------------

def draw_line(c, x1: float, y1: float, x2: float, y2: float, width: float = layout.LINE_WIDTH, hex_color: str = layout.COLOR_BLACK, cap: int = 1):
    stroke(c, hex_color)
    c.setLineWidth(width)
    c.setLineCap(cap)
    c.line(x1, y_up(y1), x2, y_up(y2))

# ----------------------------------------------------------------------

def draw_rect(c, x: float, y_top: float, w: float, h: float, hex_fill: str = None, hex_stroke: str = None, stroke_width: float = None):
    do_fill = 0
    do_stroke = 0
    if hex_fill:
        fill(c, hex_fill)
        do_fill = 1
    if hex_stroke:
        stroke(c, hex_stroke)
        if stroke_width:
            c.setLineWidth(stroke_width)
        do_stroke = 1
    c.rect(x, y_up(y_top + h), w, h, fill=do_fill, stroke=do_stroke)
