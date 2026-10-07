"""Notice bas de coupon, Light étroit 8 pt + TJ/Tw du gabarit."""

from .. import copy as texts
from .. import layout
from ..paint import draw_runs, fill


def draw(c, doc, i=0):
    fill(c, layout.COLOR)
    draw_runs(
        c, layout.NOTICE_X, layout.NOTICE1_Y[i],
        texts.NOTICE_1_RUNS, layout.FONT_NARROW, layout.SIZE_NOTICE,
        word_space_em=texts.NOTICE_1_TW,
    )
    draw_runs(
        c, layout.NOTICE_X, layout.NOTICE2_Y[i],
        texts.NOTICE_2_RUNS, layout.FONT_NARROW, layout.SIZE_NOTICE,
        word_space_em=texts.NOTICE_2_TW,
    )
