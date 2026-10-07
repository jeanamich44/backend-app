"""Caisse / agence / tél / fax à gauche, date / code à droite."""

from .. import copy as texts
from .. import layout
from ..paint import draw_right, draw_string, fill, width


def draw(c, doc, dy=0):
    if not doc.visible.middle_agence:
        return
    card = doc.card
    fill(c, layout.COLOR)
    if card.caisse:
        draw_string(
            c, layout.LABEL_X, layout.CAISSE_Y + dy, card.caisse,
            layout.FONT, layout.SIZE, max_width=layout.MAX_LINE,
        )
    if card.agence:
        draw_string(
            c, layout.LABEL_X, layout.AGENCE_Y + dy, card.agence,
            layout.FONT_BOLD, layout.SIZE, max_width=layout.MAX_LINE,
        )
    draw_string(
        c, layout.LABEL_X, layout.TEL_Y + dy, texts.LABEL_TEL,
        layout.FONT_BOLD, layout.SIZE,
    )
    if card.tel:
        gap = 4.0
        max_w = max(8.0, layout.FAX_X - layout.TEL_VAL_X - gap)
        draw_string(
            c, layout.TEL_VAL_X, layout.TEL_Y + dy, card.tel,
            layout.FONT, layout.SIZE, max_width=max_w,
        )
    draw_string(
        c, layout.FAX_X, layout.TEL_Y + dy, texts.LABEL_FAX,
        layout.FONT_BOLD, layout.SIZE,
    )
    fax_x = layout.FAX_X + width(texts.LABEL_FAX, layout.FONT_BOLD, layout.SIZE)
    if card.fax:
        draw_string(
            c, fax_x, layout.TEL_Y + dy, card.fax,
            layout.FONT, layout.SIZE, max_width=120.0,
        )
    if card.date:
        draw_right(
            c, layout.RIGHT_X, layout.DATE_Y + dy, card.date,
            layout.FONT, layout.SIZE, max_width=80.0,
        )
    if card.code:
        draw_right(
            c, layout.RIGHT_X, layout.CODE_Y + dy, card.code,
            layout.FONT, layout.SIZE, max_width=40.0,
        )
