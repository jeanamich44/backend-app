"""En-tête tableau + filets haut / sous-libellés."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill, stroke_line


def draw(c, doc):
    if not doc.visible.middle_columns:
        return
    x0, y0, x1, y1 = layout.LINE_TOP
    stroke_line(c, x0, y0, x1, y1, layout.TABLE_RULE_W, layout.COLOR)
    x0, y0, x1, y1 = layout.LINE_HEAD
    stroke_line(c, x0, y0, x1, y1, layout.TABLE_RULE_W, layout.COLOR)

    fill(c, layout.COLOR)
    bold = layout.FONT_BOLD
    size = layout.SIZE_BODY
    y = layout.COL_HEAD_Y
    yr = layout.COL_HEAD_Y_RIGHT
    draw_string(c, layout.COL_ITEM_X, y, texts.COL_ITEM, bold, size)
    draw_string(c, layout.COL_SKU_X, y, texts.COL_SKU, bold, size)
    draw_string(c, layout.COL_BARCODE_X, y, texts.COL_CODE_L1, bold, size)
    draw_string(c, layout.COL_BARCODE_X, layout.COL_BARRES_Y, texts.COL_CODE_L2, bold, size)
    draw_string(c, layout.COL_DESC_X, yr, texts.COL_DESC, bold, size)
    draw_string(c, layout.COL_SIZE_X, yr, texts.COL_SIZE, bold, size)
    draw_string(c, layout.COL_COLOR_X, yr, texts.COL_COLOR, bold, size)
    draw_string(c, layout.COL_QTY_X, yr, texts.COL_QTY, bold, size)
    draw_string(c, layout.COL_PRICE_X, yr, texts.COL_PRICE, bold, size)
