"""Numéro de ticket / caisse / date / caissier."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_refs:
        return
    card = doc.card
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LEFT_X, layout.TICKET_LABEL_Y,
        texts.LABEL_TICKET, layout.FONT_BOLD, layout.SIZE_BODY,
    )
    draw_string(
        c, layout.LEFT_X, layout.CAISSE_LABEL_Y,
        texts.LABEL_CAISSE, layout.FONT_BOLD, layout.SIZE_BODY,
    )
    draw_string(
        c, layout.DATE_LABEL_X, layout.DATE_LABEL_Y,
        texts.LABEL_DATE, layout.FONT_BOLD, layout.SIZE_BODY,
    )
    draw_string(
        c, layout.CASHIER_LABEL_X, layout.CASHIER_LABEL_Y,
        texts.LABEL_CASHIER, layout.FONT_BOLD, layout.SIZE_BODY,
    )
    draw_string(
        c, layout.VALUE_LEFT_X, layout.TICKET_VAL_Y,
        card.num_ticket, layout.FONT, layout.SIZE_BODY,
        max_width=layout.TICKET_MAX_W,
    )
    draw_string(
        c, layout.VALUE_LEFT_X, layout.CAISSE_VAL_Y,
        card.ticket_caisse, layout.FONT, layout.SIZE_BODY,
        max_width=layout.CAISSE_MAX_W,
    )
    draw_string(
        c, layout.VALUE_RIGHT_X, layout.DATE_VAL_Y,
        card.date_ticket, layout.FONT, layout.SIZE_BODY,
        max_width=layout.DATE_MAX_W,
    )
    draw_string(
        c, layout.VALUE_RIGHT_X, layout.CASHIER_VAL_Y,
        card.caissier, layout.FONT, layout.SIZE_BODY,
        max_width=layout.CASHIER_MAX_W,
    )
