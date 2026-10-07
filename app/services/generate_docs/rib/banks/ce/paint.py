from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

from app.services.generate_docs.common.paths import LOGOS_DIR

from . import layout


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


def fill(c, hex_color: str):
    color = HexColor(hex_color)
    c.setFillColor(color)
    c.setStrokeColor(color)


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
    max_width=None, justify_to=None, stroke=True,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    word_space = None
    if justify_to is not None:
        spaces = text.count(" ")
        extra = justify_to - width(text, font, size)
        if spaces and extra > 0:
            word_space = extra / spaces
    yu = y_up(y_origin)
    c.saveState()
    c._code.append("0 J")
    t = c.beginText(x, yu)
    t.setFont(font, size)
    if word_space is not None:
        t.setWordSpace(word_space)
    if stroke:
        c._code.append(f"{layout.STROKE_W:g} w")
        t._code.append(f"{layout.STROKE_W:g} w")
        t.setTextRenderMode(layout.RENDER_MODE)
    else:
        t.setTextRenderMode(0)
    t.textOut(text)
    c.drawText(t)
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


def fill_rect(c, x0: float, y0: float, x1: float, y1: float, hex_color: str):
    c.saveState()
    c.setFillColor(HexColor(hex_color))
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=0, fill=1)
    c.restoreState()


def stroke_line(c, x0: float, y: float, x1: float, width: float, hex_color: str, dash=None):
    c.setStrokeColor(HexColor(hex_color))
    c.setLineWidth(width)
    c.setLineCap(0)
    if dash:
        c.setDash(dash[0], dash[1])
    else:
        c.setDash([])
    yu = y_up(y)
    c.line(x0, yu, x1, yu)


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float, mask=None):
    c.saveState()
    c.drawImage(
        str(LOGOS_DIR / filename),
        x, y_up(y_top + h),
        width=w, height=h, mask=mask,
    )
    c.restoreState()

