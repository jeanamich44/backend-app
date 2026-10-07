"""Helpers dessin (Y ReportLab, logo PNG, filets, clip)."""

from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

from app.services.generate_docs.common.paths import LOGOS_DIR

from . import layout


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


def fill(c, hex_color: str):
    c.setFillColor(HexColor(hex_color))


def clip(text, font, size, max_width):
    text = text or ""
    if max_width is None or stringWidth(text, font, size) <= max_width:
        return text
    while text and stringWidth(text, font, size) > max_width:
        text = text[:-1]
    return text


def draw_string(c, x: float, y_origin: float, text: str, font: str, size: float, max_width=None):
    text = clip(text, font, size, max_width)
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text)


def draw_centred(c, x: float, y_origin: float, text: str, font: str, size: float, max_width=None):
    text = clip(text, font, size, max_width)
    c.setFont(font, size)
    c.drawCentredString(x, y_up(y_origin), text)


def fill_rect(c, x0, y0, x1, y1, hex_color: str):
    c.saveState()
    c.setFillColor(HexColor(hex_color))
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=0, fill=1)
    c.restoreState()


def stroke_line(c, x0, y0, x1, y1, width, hex_color="#000000", dash=None, cap=0):
    c.saveState()
    c.setStrokeColor(HexColor(hex_color))
    c.setLineWidth(width)
    c.setLineCap(cap)
    if dash:
        c.setDash(list(dash), 0)
    c.line(x0, y_up(y0), x1, y_up(y1))
    c.restoreState()


def wrap_lines(text: str, font: str, size: float, max_width: float) -> list[str]:
    lines = []
    current = ""
    for word in (text or "").split():
        trial = word if not current else f"{current} {word}"
        if stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def draw_paragraphs(
    c,
    x: float,
    y_top: float,
    text: str,
    font: str,
    size: float,
    leading: float,
    max_width: float,
    hex_color: str,
):
    """Un paragraphe par ligne source ; lignes pleines justifiées, dernière à gauche."""
    color = HexColor(hex_color)
    y = y_top
    for paragraph in (text or "").split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            y += leading
            continue
        lines = wrap_lines(paragraph, font, size, max_width)
        last = len(lines) - 1
        for i, line in enumerate(lines):
            extra = 0.0
            if i != last:
                spaces = line.count(" ")
                natural = stringWidth(line, font, size)
                if spaces and natural < max_width:
                    extra = (max_width - natural) / spaces
            t = c.beginText(x, y_up(y))
            t.setFont(font, size)
            t.setFillColor(color)
            t.setWordSpace(extra)
            t.textOut(line)
            c.drawText(t)
            y += leading


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float):
    path = LOGOS_DIR / filename
    c.drawImage(str(path), x, y_up(y_top + h), width=w, height=h, mask="auto")
