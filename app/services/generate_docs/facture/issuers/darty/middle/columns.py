"""En-têtes de colonnes + filets tableau."""

from .. import copy as texts
from .. import layout
from ..chrome import vectors
from ..paint import draw_strokes, draw_string, fill, shift_strokes


def draw(c, doc):
    if not doc.visible.middle_columns:
        return
    n = layout.n_items(doc.card)
    dy = layout.table_shift(doc.card)
    draw_strokes(c, vectors.TABLE_HEADER_STROKES)
    draw_strokes(c, vectors.TABLE_ROW_TOP_STROKES)
    for i in range(1, n):
        draw_strokes(
            c, shift_strokes(vectors.TABLE_ROW_TOP_STROKES, i * layout.ROW_PITCH),
        )
    draw_strokes(c, shift_strokes(vectors.TABLE_BOTTOM_STROKES, dy))
    fill(c, layout.COLOR)
    y = layout.COL_Y
    draw_string(c, layout.COL_REF_X, y, texts.COL_REF, layout.FONT_BOLD, layout.SIZE_COL)
    draw_string(c, layout.COL_QTE_X, y, texts.COL_QTE, layout.FONT_BOLD, layout.SIZE_COL)
    draw_string(c, layout.COL_LIB_X, y, texts.COL_LIB, layout.FONT_BOLD, layout.SIZE_COL)
    draw_string(
        c, layout.COL_DATE_X, layout.COL_Y_TOP,
        texts.COL_DATE, layout.FONT_BOLD, layout.SIZE_COL,
    )
    draw_string(
        c, layout.COL_DELIV_X, layout.COL_Y_BOT,
        texts.COL_DELIV, layout.FONT_BOLD, layout.SIZE_COL,
    )
    draw_string(c, layout.COL_HT_X, y, texts.COL_HT, layout.FONT_BOLD, layout.SIZE_COL)
    draw_string(
        c, layout.COL_BASE_X, layout.COL_Y_TOP,
        texts.COL_BASE, layout.FONT_BOLD, layout.SIZE_COL,
    )
    draw_string(
        c, layout.COL_TVA_X, layout.COL_Y_BOT,
        texts.COL_TVA, layout.FONT_BOLD, layout.SIZE_COL,
    )
    draw_string(c, layout.COL_TTC_X, y, texts.COL_TTC, layout.FONT_BOLD, layout.SIZE_COL)
