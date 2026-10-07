"""Notice d'utilisation (texte live, Arial 9 pt, justifiée sur les lignes pleines)."""

from .. import layout
from ..paint import draw_paragraphs


def draw(c, doc, dy=0):
    if not doc.visible.middle_notice:
        return
    text = doc.card.notice
    if not text:
        return
    draw_paragraphs(
        c, layout.LABEL_X, layout.NOTICE_Y + dy, text,
        layout.FONT, layout.SIZE, layout.NOTICE_LEADING,
        layout.NOTICE_W, layout.COLOR,
    )
