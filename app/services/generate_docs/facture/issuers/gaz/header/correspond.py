"""Bandeau teal : à quoi correspond cette facture."""

from .. import copy as texts
from .. import layout
from ..chrome.correspond_paths import CORRESPOND_EVEN_ODD, CORRESPOND_OPS
from ..paint import draw_string, fill, fill_ops


def draw(c, doc):
    if not doc.visible.header_correspond:
        return
    fill_ops(c, CORRESPOND_OPS, layout.TEAL, even_odd=CORRESPOND_EVEN_ODD)
    fill(c, layout.COLOR)
    draw_string(
        c, layout.CORRESPOND_TITLE_X, layout.CORRESPOND_TITLE_Y,
        texts.CORRESPOND_TITLE, layout.FONT_BOLD, layout.SIZE_CORRESPOND_TITLE,
        max_width=layout.CORRESPOND_TITLE_MAX_W,
    )
    fill(c, layout.COLOR_WHITE)
    draw_string(
        c, layout.CORRESPOND_BODY_X, layout.CORRESPOND_BODY_Y[0],
        texts.CORRESPOND_BODY[0], layout.FONT, layout.SIZE_CORRESPOND_BODY,
        max_width=layout.CORRESPOND_BODY_MAX_W,
        word_space=layout.CORRESPOND_BODY_TW,
    )
    draw_string(
        c, layout.CORRESPOND_BODY_X, layout.CORRESPOND_BODY_Y[1],
        texts.CORRESPOND_BODY[1], layout.FONT, layout.SIZE_CORRESPOND_BODY,
        max_width=layout.CORRESPOND_BODY_MAX_W,
    )
