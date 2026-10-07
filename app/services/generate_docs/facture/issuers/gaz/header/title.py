"""Bandeau titre + date/n° + sous-titre italique."""

from .. import copy as texts
from .. import layout, rules
from ..chrome.header_paths import BANNER_EVEN_ODD, BANNER_OPS
from ..paint import draw_string, fill, fill_ops


def draw(c, doc):
    if not doc.visible.header_title:
        return
    fill_ops(c, BANNER_OPS, layout.BLUE, even_odd=BANNER_EVEN_ODD)
    fill(c, layout.COLOR_WHITE)
    draw_string(
        c, layout.TITLE_X, layout.TITLE_Y,
        texts.TITLE, layout.FONT_BOLD, layout.SIZE_TITLE,
        max_width=layout.TITLE_MAX_W,
    )
    draw_string(
        c, layout.BANNER_META_X, layout.BANNER_META_Y,
        rules.banner_meta(doc.card), layout.FONT_HB, layout.SIZE_BANNER,
        max_width=layout.BANNER_META_MAX_W,
    )
    fill(c, layout.COLOR)
    for y, line in zip(layout.ITALIC_Y, texts.SUBTITLE):
        draw_string(
            c, layout.ITALIC_X, y, line,
            layout.FONT_ITALIC, layout.SIZE_ITALIC,
            max_width=layout.ITALIC_MAX_W,
        )
