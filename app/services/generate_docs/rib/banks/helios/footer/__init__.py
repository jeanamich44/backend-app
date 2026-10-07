"""Mentions légales Helios / Okali, bas de page."""

from .. import layout
from ..paint import draw_string, fill, wrap_lines


def draw(c, doc):
    if not doc.visible.footer or not doc.visible.footer_legal:
        return
    text = doc.footer.legal
    if not text:
        return
    fill(c, layout.COLOR)
    y = layout.LEGAL_Y
    font, size, max_w = layout.FONT, layout.SIZE_BODY, layout.LEGAL_W
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            y += layout.LEGAL_LEADING
            continue
        for line in wrap_lines(paragraph, font, size, max_w):
            draw_string(c, layout.LEGAL_X, y, line, font, size, max_width=max_w)
            y += layout.LEGAL_LEADING
