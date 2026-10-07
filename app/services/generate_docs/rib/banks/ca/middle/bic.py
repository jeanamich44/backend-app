"""BIC / SWIFT : label à gauche, valeur compacte à droite."""

from .. import copy as texts
from .. import layout
from ..paint import draw_right, draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_bic:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_X, layout.BIC_Y + dy,
        texts.LABEL_BIC, layout.FONT_BOLD, layout.SIZE,
    )
    if doc.card.bic:
        draw_right(
            c, layout.RIGHT_X, layout.BIC_Y + dy, doc.card.bic,
            layout.FONT, layout.SIZE, max_width=layout.BIC_W,
        )
