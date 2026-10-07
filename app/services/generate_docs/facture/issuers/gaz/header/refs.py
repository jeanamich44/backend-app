"""Référence client + n° compte de contrat."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_refs:
        return
    fill(c, layout.COLOR_BLUE)
    draw_string(
        c, layout.REF_X, layout.CLIENT_LABEL_Y,
        texts.CLIENT_LABEL, layout.FONT_BOLD, layout.SIZE_REF,
        max_width=layout.REF_MAX_W,
    )
    draw_string(
        c, layout.REF_X, layout.CONTRAT_LABEL_Y,
        texts.CONTRAT_LABEL, layout.FONT_BOLD, layout.SIZE_REF,
        max_width=layout.REF_MAX_W,
    )
    fill(c, layout.COLOR)
    draw_string(
        c, layout.CLIENT_VAL_X, layout.CLIENT_LABEL_Y,
        rules.client_value(doc.card), layout.FONT, layout.SIZE_REF,
        max_width=layout.NUM_MAX_W,
    )
    draw_string(
        c, layout.CONTRAT_VAL_X, layout.CONTRAT_LABEL_Y,
        rules.contrat_value(doc.card), layout.FONT, layout.SIZE_REF,
        max_width=layout.NUM_MAX_W,
    )
