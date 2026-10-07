"""Domiciliation : label outlined + adresse établissement."""

from .. import copy as texts
from .. import layout
from .. import rules
from ..paint import draw_label, draw_string, draw_svg, fill


def draw(c, doc):
    if not doc.visible.middle_domiciliation:
        return
    draw_label(c, layout.LABEL_DOM)
    text = doc.card.domiciliation
    if not text:
        return
    if text == texts.DOMICILIATION or rules.clean("middle_domiciliation_text", text) == texts.DOMICILIATION:
        draw_svg(
            c, layout.DOM_SVG,
            layout.DOM_SVG_X, layout.DOM_SVG_Y_TOP,
            layout.DOM_SVG_W, layout.DOM_SVG_H,
        )
        return
    fill(c, layout.COLOR_DOM)
    draw_string(
        c, layout.DOM_X, layout.DOM_Y, text,
        layout.FONT, layout.FONT_SIZE,
        max_width=layout.DOM_W,
    )
