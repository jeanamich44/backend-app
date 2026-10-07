"""Titre Détails + en-tête de colonnes."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill, fill_rect


def draw(c, doc, plan):
    if not plan.columns or not doc.visible.middle_columns:
        return
    header = plan.header or {}
    left, right = layout.RULE_X
    fill_rect(
        c, left, header["head_rule"], right,
        header["head_rule"] + layout.RULE_H, layout.COLOR_RULE_LIGHT,
    )
    fill(c, layout.COLOR)
    uni = layout.FONT_UNI
    small = layout.SIZE_SMALL
    draw_string(
        c, layout.DETAILS_X, header["details"],
        texts.DETAILS, uni, layout.SIZE_DETAILS,
    )
    y = header["col_head"]
    draw_string(c, layout.HEAD_DESC_X, y, texts.COL_DESC, uni, small)
    draw_string(c, layout.HEAD_QTE_X, y, texts.COL_QTE, uni, small)
    draw_string(c, layout.HEAD_PU_HT_X, y, texts.COL_PU, uni, small)
    draw_string(c, layout.HEAD_TVA_X, y, texts.COL_TVA, uni, small)
    draw_string(c, layout.HEAD_PU_TTC_X, y, texts.COL_PU, uni, small)
    draw_string(c, layout.HEAD_TOTAL_X, y, texts.COL_TOTAL, uni, small)
    y = header["col_sub"]
    draw_string(c, layout.HEAD_HT_X, y, texts.COL_HT, uni, small)
    draw_string(c, layout.HEAD_TTC_X, y, texts.COL_TTC, uni, small)
    draw_string(c, layout.HEAD_TOTAL_TTC_X, y, texts.COL_TTC, uni, small)
