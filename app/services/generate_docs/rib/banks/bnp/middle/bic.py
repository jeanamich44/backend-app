"""Case BIC : cadre vecteur + label + valeur centrée."""

from .. import copy as texts
from .. import layout
from ..paint import draw_centred, draw_string, fill, stroke_rect


def draw(c, doc, dy=0):
    if not doc.visible.middle_bic:
        return
    x0, y0, x1, y1 = layout.BIC_BOX
    stroke_rect(c, x0, y0 + dy, x1, y1 + dy, layout.BOX_STROKE, fill_hex="#ffffff")
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_BIC_XY[0], layout.LABEL_BIC_XY[1] + dy,
        texts.LABEL_BIC, layout.FONT, layout.FONT_SIZE,
    )
    draw_string(
        c, layout.REF_BIC_XY[0], layout.REF_BIC_XY[1] + dy,
        texts.REF_2, layout.FONT, layout.FONT_REF_SIZE,
    )
    if doc.card.bic:
        draw_centred(
            c, layout.BIC_CX, layout.BIC_Y + dy, doc.card.bic,
            layout.FONT_BOLD, layout.FONT_SIZE,
            max_width=layout.BIC_W,
        )
