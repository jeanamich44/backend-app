"""Helpers dessin (Y ReportLab, fill-only, wordmark)."""

from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import FILL_NON_ZERO

from . import layout


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
    max_width=None, char_space=0.0,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    c.setFont(font, size)
    y = y_up(y_origin)
    if char_space:
        cursor = x
        for ch in text:
            c.drawString(cursor, y, ch)
            cursor += width(ch, font, size) + char_space
    else:
        c.drawString(x, y, text)


def draw_right(c, x: float, y_origin: float, text: str, font: str, size: float):
    if not text:
        return
    c.setFont(font, size)
    c.drawRightString(x, y_up(y_origin), text)


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


def clip_rect(c, x0: float, y0: float, x1: float, y1: float):
    """Clip Y depuis le haut (PyMuPDF)."""
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    path = c.beginPath()
    path.rect(left, y_up(bot), right - left, bot - top)
    c.clipPath(path, stroke=0, fill=0)


def fill_fills(c, fills, hex_color: str):
    """Rejoue les fills du Form1 (sous-chemins = trous nonzero)."""
    c.saveState()
    c.setFillColor(HexColor(hex_color))
    for fill_ops in fills:
        path = c.beginPath()
        for sub in fill_ops:
            started = False
            for item in sub:
                kind = item[0]
                if kind == "m":
                    if started:
                        path.close()
                    path.moveTo(item[1], y_up(item[2]))
                    started = True
                elif kind == "l":
                    path.lineTo(item[1], y_up(item[2]))
                elif kind == "c":
                    a, b, d = item[1], item[2], item[3]
                    path.curveTo(
                        a[0], y_up(a[1]),
                        b[0], y_up(b[1]),
                        d[0], y_up(d[1]),
                    )
                elif kind == "h":
                    path.close()
                    started = False
        c.drawPath(path, stroke=0, fill=1, fillMode=FILL_NON_ZERO)
    c.restoreState()
