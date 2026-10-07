"""Encadré TVA déclarée par Amazon (chrome émetteur)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_vat:
        return
    fill(c, layout.COLOR)
    y_by, y_num = layout.VAT_Y
    draw_string(
        c, layout.VAT_LABEL_X, y_by,
        texts.VAT_BY, layout.FONT_UNI, layout.SIZE_SMALL,
    )
    draw_string(
        c, layout.VAT_VALUE_X, y_by,
        texts.VAT_ENTITY, layout.FONT_UNI, layout.SIZE_SMALL,
    )
    draw_string(
        c, layout.VAT_LABEL_X, y_num,
        texts.VAT_LABEL, layout.FONT_UNI, layout.SIZE_SMALL,
    )
    draw_string(
        c, layout.VAT_VALUE_X, y_num,
        texts.VAT_NUMBER, layout.FONT_UNI, layout.SIZE_SMALL,
    )
