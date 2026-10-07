"""En-tête tableau : bandes grises D3–D9 + libellés."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill, fill_rect


def _cell(c, xs):
    fill_rect(c, xs[0], layout.COL_Y0, xs[1], layout.COL_Y1, layout.COLOR_GRAY)


def draw(c, doc):
    if not doc.visible.middle_columns:
        return
    for xs in (
        layout.CELL_ARTICLE, layout.CELL_TAILLE, layout.CELL_NOM,
        layout.CELL_QTE, layout.CELL_HT, layout.CELL_TTC, layout.CELL_TOTAL,
    ):
        _cell(c, xs)

    fill(c, layout.COLOR)
    y = layout.COL_HEAD_Y
    draw_string(c, layout.COL_ARTICLE_X, y, texts.COL_ARTICLE, layout.FONT_BOLD, layout.SIZE_COL)
    draw_string(c, layout.COL_TAILLE_X, y, texts.COL_TAILLE, layout.FONT_BOLD, layout.SIZE_COL)
    draw_string(c, layout.COL_NOM_X, y, texts.COL_NOM, layout.FONT_BOLD, layout.SIZE_COL)
    draw_string(c, layout.COL_QTE_X, y, texts.COL_QTE, layout.FONT_BOLD, layout.SIZE_COL)

    y0, y1, y2 = layout.PRICE_HEAD_Y
    ht0, ht1, ht2 = layout.PRICE_HT_X
    ttc0, ttc1, ttc2 = layout.PRICE_TTC_X
    tot0, tot1 = layout.PRICE_TOTAL_X
    sz = layout.SIZE_PRICE_HEAD
    bold = layout.FONT_BOLD
    draw_string(c, ht0, y0, texts.COL_PU, bold, sz)
    draw_string(c, ht1, y1, texts.COL_HT, bold, sz)
    draw_string(c, ht2, y2, texts.COL_EUR, bold, sz)
    draw_string(c, ttc0, y0, texts.COL_PU, bold, sz)
    draw_string(c, ttc1, y1, texts.COL_TTC, bold, sz)
    draw_string(c, ttc2, y2, texts.COL_EUR, bold, sz)
    draw_string(c, tot0, y0, texts.COL_PRIX_TOTAL, bold, sz)
    draw_string(c, tot1, y1, texts.COL_EUR, bold, sz)
