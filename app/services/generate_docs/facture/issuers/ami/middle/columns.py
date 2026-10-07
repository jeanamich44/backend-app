"""Bandeau Description / Quantité / Prix à / Coût + filets D6–D8."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, extend_down, fill, fill_rect, fill_subpaths
from . import vectors


def draw(c, doc):
    if not doc.visible.middle_columns:
        return
    extra = layout.table_shift(len(doc.card.items or ()))
    fill_rect(c, layout.TABLE_X0, layout.HEAD_Y0, layout.TABLE_X1, layout.HEAD_Y1, layout.COLOR_HEAD)
    fill(c, layout.COLOR_WHITE)
    labels = (texts.COL_DESC, texts.COL_QTY, texts.COL_PRICE, texts.COL_COST)
    for text, x, y in zip(labels, layout.COL_TEXT_X, layout.HEAD_TEXT_Y):
        draw_string(c, x, y, text, layout.FONT, layout.SIZE_COL)
    for path in (vectors.VLINE_QTY, vectors.VLINE_PRICE, vectors.VLINE_COST):
        fill_subpaths(c, extend_down(path, extra), vectors.COLOR_GRID)
