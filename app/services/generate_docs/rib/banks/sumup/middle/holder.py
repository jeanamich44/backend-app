"""Colonne gauche : Account holder details."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_holder:
        return
    card = doc.card
    x = layout.LEFT_X
    fill(c, layout.COLOR)
    draw_string(
        c, x, layout.SECTION_Y + dy, texts.HOLDER_TITLE,
        layout.FONT_BOLD, layout.SIZE_SECTION,
        max_width=layout.COL_W,
    )
    draw_string(
        c, x, layout.LABEL1_Y + dy, texts.LABEL_NAME,
        layout.FONT, layout.SIZE_LABEL,
        max_width=layout.COL_W,
    )
    if card.titulaire_nom:
        draw_string(
            c, x, layout.VALUE1_Y + dy, card.titulaire_nom,
            layout.FONT_BOLD, layout.SIZE_VALUE,
            max_width=layout.COL_W,
        )
    draw_string(
        c, x, layout.LABEL2_Y + dy, texts.LABEL_ADDRESS,
        layout.FONT, layout.SIZE_LABEL,
        max_width=layout.COL_W,
    )
    y = layout.VALUE2_Y + dy
    for line in (card.titulaire_adresse, card.titulaire_ville, card.titulaire_pays):
        if line:
            draw_string(
                c, x, y, line,
                layout.FONT_BOLD, layout.SIZE_VALUE,
                max_width=layout.COL_W,
            )
        y += layout.ADDR_LEADING
