"""Notice FR + EN, une ligne chacune (pas de wrap)."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, i=0):
    if not doc.visible.middle_notice:
        return
    text = doc.card.notice
    if not text:
        return
    fill(c, layout.NAVY)
    y = layout.NOTICE_Y + layout.dy(i)
    font, size = layout.FONT, layout.NOTICE_SIZE
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    for n, paragraph in enumerate(paragraphs):
        draw_string(
            c, layout.NOTICE_X, y, paragraph, font, size,
            max_width=layout.NOTICE_W,
        )
        if n == 0 and i == 2:
            y += 5.0
        else:
            y += layout.NOTICE_LEADING
