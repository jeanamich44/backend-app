"""IBAN / BIC : titre section 2 Tr, labels 2 Tr, valeurs compactes fill-only."""

from .. import copy as texts
from .. import layout
from .. import rib
from ..paint import draw_label, draw_value


def draw(c, doc, dy=0):
    vis = doc.visible
    if vis.middle_iban or vis.middle_bic:
        draw_label(
            c, layout.INTL_X, layout.INTL_Y + dy, texts.INTL_TITLE,
            layout.FONT, layout.INTL_SIZE,
            max_width=layout.INTL_W,
        )
    if vis.middle_iban:
        draw_label(
            c, layout.IBAN_HEAD_X, layout.IBAN_HEAD_Y + dy, texts.LABEL_IBAN,
            layout.FONT, layout.FIELD_SIZE,
        )
        iban = rib.compact(doc.card.iban)
        if iban:
            draw_value(
                c, layout.IBAN_VAL_X, layout.IBAN_VAL_Y + dy, iban,
                layout.FONT, layout.FIELD_SIZE,
                max_width=layout.IBAN_W,
            )
    if vis.middle_bic:
        draw_label(
            c, layout.BIC_HEAD_X, layout.IBAN_HEAD_Y + dy, texts.LABEL_BIC,
            layout.FONT, layout.FIELD_SIZE,
        )
        if doc.card.bic:
            draw_value(
                c, layout.BIC_VAL_X, layout.IBAN_VAL_Y + dy, doc.card.bic,
                layout.FONT, layout.FIELD_SIZE,
                max_width=layout.BIC_W,
            )
