"""Colonne droite : Account details (date, institution, IBAN, BIC)."""

from .. import copy as texts
from .. import layout
from .. import rib
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_account:
        return
    card = doc.card
    x = layout.RIGHT_X
    fill(c, layout.COLOR)
    draw_string(
        c, x, layout.SECTION_Y + dy, texts.ACCOUNT_TITLE,
        layout.FONT_BOLD, layout.SIZE_SECTION,
        max_width=layout.COL_W,
    )
    draw_string(
        c, x, layout.LABEL1_Y + dy, texts.LABEL_OPENING,
        layout.FONT, layout.SIZE_LABEL,
        max_width=layout.COL_W,
    )
    if card.date_ouverture:
        draw_string(
            c, x, layout.VALUE1_Y + dy, card.date_ouverture,
            layout.FONT_BOLD, layout.SIZE_VALUE,
            max_width=layout.COL_W,
        )
    draw_string(
        c, x, layout.LABEL2_Y + dy, texts.LABEL_INSTITUTION,
        layout.FONT, layout.SIZE_LABEL,
        max_width=layout.COL_W,
    )
    if card.institution:
        draw_string(
            c, x, layout.VALUE2_Y + dy, card.institution,
            layout.FONT_BOLD, layout.SIZE_VALUE,
            max_width=layout.COL_W,
        )
    draw_string(
        c, x, layout.IBAN_LABEL_Y + dy, texts.LABEL_IBAN,
        layout.FONT, layout.SIZE_LABEL,
        max_width=layout.COL_W,
    )
    if card.iban:
        draw_string(
            c, x, layout.IBAN_VALUE_Y + dy, rib.compact(card.iban),
            layout.FONT_BOLD, layout.SIZE_VALUE,
            max_width=layout.COL_W,
        )
    draw_string(
        c, x, layout.BIC_LABEL_Y + dy, texts.LABEL_BIC,
        layout.FONT, layout.SIZE_LABEL,
        max_width=layout.COL_W,
    )
    if card.bic:
        draw_string(
            c, x, layout.BIC_VALUE_Y + dy, rib.compact(card.bic),
            layout.FONT_BOLD, layout.SIZE_VALUE,
            max_width=layout.COL_W,
        )
