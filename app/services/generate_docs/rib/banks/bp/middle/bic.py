"""BIC : label mixte + valeur compacte (texte live)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_bic:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_X, layout.BIC_Y + dy,
        texts.LABEL_BIC, layout.FONT, layout.SIZE,
    )
    if doc.card.bic:
        draw_string(
            c, layout.VALUE_X, layout.BIC_Y + dy, doc.card.bic,
            layout.FONT, layout.SIZE, max_width=layout.MAX_LINE,
        )
