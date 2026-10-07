"""Adresse agence + téléphone (ZapfDingbats '%' comme le gabarit)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, draw_zapf_pct, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_domiciliation:
        return
    card = doc.card
    fill(c, layout.COLOR)
    draw_string(
        c, layout.DOM_X, layout.DOM_LABEL_Y + dy, texts.LABEL_DOM,
        layout.VALUE_FONT, layout.SIZE_VALUE, max_width=layout.DOM_W,
    )
    rows = (card.agence, card.domiciliation_rue, card.domiciliation_ville)
    for i, value in enumerate(rows):
        if not value:
            continue
        draw_string(
            c, layout.DOM_X,
            layout.DOM_Y + i * layout.DOM_LEADING + dy,
            value, layout.ADDR_FONT, layout.SIZE_LABEL,
            max_width=layout.DOM_W,
        )
    if card.phone:
        draw_zapf_pct(
            c, layout.PHONE_DINGBAT_X, layout.PHONE_Y + dy, layout.DINGBAT_SIZE,
        )
        draw_string(
            c, layout.PHONE_X, layout.PHONE_Y + dy, card.phone + " ",
            layout.ADDR_FONT, layout.SIZE_LABEL, max_width=layout.DOM_W,
        )
