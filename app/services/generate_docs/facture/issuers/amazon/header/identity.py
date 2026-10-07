"""Identité sous le logo (capitales)."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_identity:
        return
    card = doc.card
    fill(c, layout.COLOR)
    lines = (
        (card.nom or "").upper(),
        (card.adresse or "").upper(),
        (card.cp_ville or "").upper(),
        card.pays or "",
    )
    y = layout.ID_Y0
    for line in lines:
        draw_string(
            c, layout.ID_X, y, line,
            layout.FONT_UNI, layout.SIZE_BODY,
            max_width=layout.ID_MAX_W,
        )
        y += layout.ID_PITCH
