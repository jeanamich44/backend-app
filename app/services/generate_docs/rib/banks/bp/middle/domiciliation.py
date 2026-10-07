"""Domiciliation : label + agence, ligne centrée (texte live, Arial Bold 9 pt)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_centred, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_domiciliation:
        return
    value = (doc.card.domiciliation or "").strip()
    text = f"{texts.LABEL_DOM} {value}".strip() if value else texts.LABEL_DOM
    fill(c, layout.COLOR)
    draw_centred(
        c, layout.PAGE_W / 2, layout.DOM_Y + dy, text,
        layout.FONT_BOLD, layout.DOM_SIZE,
        max_width=layout.MAX_LINE,
    )
