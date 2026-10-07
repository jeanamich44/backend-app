"""Notice d'utilisation (texte live, Open Sans SemiBold 9.6 pt, à gauche)."""

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
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            y += layout.NOTICE_LEADING
            continue
        for line in wrap_lines(
            paragraph, layout.FONT, layout.SIZE, layout.NOTICE_W,
        ):
            draw_string(c, layout.LABEL_X, y, line, layout.FONT, layout.SIZE)
            y += layout.NOTICE_LEADING
