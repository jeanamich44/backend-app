"""En-têtes Article / Description / Quantité / Prix / Total + filets."""

from .. import copy as texts
from .. import layout
from ..chrome import vectors
from ..paint import draw_string, fill, stroke_seg


def draw(c, doc):
    if not doc.visible.middle_columns:
        return
    n = layout.n_items(doc.card)
    stroke_seg(c, vectors.COL_LINE, layout.RULE_W, layout.COLOR)
    for i in range(n):
        stroke_seg(
            c,
            layout.shift_line(vectors.ROW_LINE, i * layout.ROW_PITCH),
            layout.RULE_W,
            layout.COLOR,
        )
    fill(c, layout.COLOR)
    y = layout.COL_Y
    draw_string(c, layout.COL_ARTICLE_X, y, texts.COL_ARTICLE, layout.FONT_BOLD, layout.SIZE_BODY)
    draw_string(c, layout.COL_DESC_X, y, texts.COL_DESC, layout.FONT_BOLD, layout.SIZE_BODY)
    draw_string(c, layout.COL_QTE_X, y, texts.COL_QTE, layout.FONT_BOLD, layout.SIZE_BODY)
    draw_string(c, layout.COL_PRIX_X, y, texts.COL_PRIX, layout.FONT_BOLD, layout.SIZE_BODY)
    draw_string(c, layout.COL_TOTAL_X, y, texts.COL_TOTAL, layout.FONT_BOLD, layout.SIZE_BODY)
