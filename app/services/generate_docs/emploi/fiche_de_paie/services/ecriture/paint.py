from reportlab.lib.colors import HexColor

from . import layout

# ----------------------------------------------------------------------


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


def stroke_line(c, x0: float, y0: float, x1: float, y1: float, width: float = 0.24, hex_color: str = layout.COLOR_BLACK, line_cap: int = 1):
    c.saveState()
    c.setStrokeColor(HexColor(hex_color))
    c.setLineWidth(width)
    c.setLineCap(line_cap)
    c.line(x0, y_up(y0), x1, y_up(y1))
    c.restoreState()


def draw_rect(c, x: float, y: float, w: float, h: float, fill_color: str | None = None, stroke_color: str | None = layout.COLOR_BLACK, stroke_width: float = 0.24):
    c.saveState()
    if fill_color:
        c.setFillColor(HexColor(fill_color))
    if stroke_color:
        c.setStrokeColor(HexColor(stroke_color))
        c.setLineWidth(stroke_width)
    c.rect(x, y_up(y + h), w, h, fill=bool(fill_color), stroke=bool(stroke_color))
    c.restoreState()


def draw_string(c, x: float, y: float, text: str, font: str, size: float, hex_color: str = layout.COLOR_BLACK, char_space: float = 0.0, word_space: float = 0.0):
    if not text:
        return
    c.saveState()
    if char_space != 0.0 or word_space != 0.0:
        t = c.beginText(x, y_up(y))
        t.setFont(font, size)
        t.setFillColor(HexColor(hex_color))
        if char_space != 0.0:
            t.setCharSpace(char_space)
        if word_space != 0.0:
            t.setWordSpace(word_space)
        t.textOut(text)
        c.drawText(t)
    else:
        c.setFont(font, size)
        c.setFillColor(HexColor(hex_color))
        c.drawString(x, y_up(y), text)
    c.restoreState()


def draw_centred(c, x: float, y: float, text: str, font: str, size: float, hex_color: str = layout.COLOR_BLACK):
    if not text:
        return
    c.saveState()
    c.setFont(font, size)
    c.setFillColor(HexColor(hex_color))
    c.drawCentredString(x, y_up(y), text)
    c.restoreState()


def draw_right(c, x: float, y: float, text: str, font: str, size: float, hex_color: str = layout.COLOR_BLACK):
    if not text:
        return
    c.saveState()
    c.setFont(font, size)
    c.setFillColor(HexColor(hex_color))
    c.drawRightString(x, y_up(y), text)
    c.restoreState()
