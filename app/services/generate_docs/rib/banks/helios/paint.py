"""Helpers dessin (Y ReportLab, PNG alpha, fill / fill+stroke 2 Tr)."""

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
    max_width=None, stroke=False, times=1,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    c.setFont(font, size)
    if stroke:
        c.setLineWidth(layout.STROKE_W)
        mode = 2
    else:
        c.setLineWidth(1)
        mode = 0
    y = y_up(y_origin)
    for _ in range(times):
        c.drawString(x, y, text, mode=mode)
    if stroke:
        c.setLineWidth(1)


def draw_label(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None,
):
    """Labels / notes du gabarit : Helvetica fill-only, peint deux fois."""
    draw_string(c, x, y_origin, text, font, size, max_width=max_width, times=2)


def draw_value(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None,
):
    """7 valeurs du gabarit : Helvetica + 2 Tr 0.45, deux fois."""
    fill(c, layout.COLOR)
    draw_string(c, x, y_origin, text, font, size, max_width=max_width, stroke=True, times=2)


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


def draw_centered(
    c, x0: float, x1: float, y_origin: float, text: str, font: str, size: float,
    max_width=None, stroke=False, times=1,
):
    limit = max_width if max_width is not None else (x1 - x0)
    text = clip(text, font, size, limit)
    if not text:
        return
    x = x0 + (x1 - x0 - width(text, font, size)) / 2.0
    draw_string(c, x, y_origin, text, font, size, stroke=stroke, times=times)


def draw_centered_label(c, x0: float, x1: float, y_origin: float, text: str, font: str, size: float):
    draw_centered(c, x0, x1, y_origin, text, font, size, times=2)


def draw_centered_value(c, x0: float, x1: float, y_origin: float, text: str, font: str, size: float):
    text = clip(text, font, size, x1 - x0)
    if not text:
        return
    x = x0 + (x1 - x0 - width(text, font, size)) / 2.0
    draw_value(c, x, y_origin, text, font, size)


def fill_rect(c, x: float, y0: float, w: float, y1: float, hex_color: str):
    c.saveState()
    c.setFillColor(HexColor(hex_color))
    top, bot = min(y0, y1), max(y0, y1)
    c.rect(x, y_up(bot), w, bot - top, stroke=0, fill=1)
    c.restoreState()


def fill_closed_path(c, items, hex_color: str, dy=0):
    """Rejoue un contour rempli du gabarit (Y PyMuPDF)."""
    path = c.beginPath()
    started = False
    for item in items:
        kind = item[0]
        if kind == "c":
            p1, p2, p3, p4 = item[1], item[2], item[3], item[4]
            if not started:
                path.moveTo(p1[0], y_up(p1[1] + dy))
                started = True
            path.curveTo(
                p2[0], y_up(p2[1] + dy),
                p3[0], y_up(p3[1] + dy),
                p4[0], y_up(p4[1] + dy),
            )
        elif kind == "l":
            a, b = item[1], item[2]
            if not started:
                path.moveTo(a[0], y_up(a[1] + dy))
                started = True
            path.lineTo(b[0], y_up(b[1] + dy))
    path.close()
    c.saveState()
    c.setFillColor(HexColor(hex_color))
    c.drawPath(path, stroke=0, fill=1)
    c.restoreState()


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float, mask="auto"):
    c.drawImage(
        str(LOGOS_DIR / filename),
        x, y_up(y_top + h),
        width=w, height=h, mask=mask,
    )
