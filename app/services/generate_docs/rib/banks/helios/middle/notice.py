"""Notice d'usage en tête de page, à gauche, ragged."""

from .. import layout
from ..paint import draw_string, fill, wrap_lines


def draw(c, doc, dy=0):
    if not doc.visible.middle_notice:
        return
    text = doc.card.notice
    if not text:
        return
    fill(c, layout.COLOR)
    y = layout.NOTICE_Y + dy
    font, size, max_w = layout.FONT, layout.SIZE_BODY, layout.NOTICE_W
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            y += layout.NOTICE_LEADING
            continue
        for line in wrap_lines(paragraph, font, size, max_w):
            draw_string(c, layout.NOTICE_X, y, line, font, size, max_width=max_w)
            y += layout.NOTICE_LEADING
