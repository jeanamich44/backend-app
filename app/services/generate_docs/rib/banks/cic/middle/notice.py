"""Notice d'usage : wrap + justification (Tw), dernière ligne à gauche."""

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
    font, size, max_w = layout.LABEL_FONT, layout.SIZE_LABEL, layout.NOTICE_W
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            y += layout.NOTICE_LEADING
            continue
        lines = wrap_lines(paragraph, font, size, max_w)
        last = len(lines) - 1
        for i, line in enumerate(lines):
            draw_string(
                c, layout.NOTICE_X, y, line, font, size,
                max_width=max_w,
                justify_to=max_w if i < last else None,
            )
            y += layout.NOTICE_LEADING
