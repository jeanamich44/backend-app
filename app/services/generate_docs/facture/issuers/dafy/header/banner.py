from .. import copy as texts
from .. import layout
from ..chrome import vectors
from ..paint import draw_chrome, draw_string, fill, fill_subpaths


def draw(c, doc):
    if not doc.visible.header_banner:
        return
    draw_chrome(
        c, layout.PHONE_FILE,
        layout.PHONE_X, layout.PHONE_Y,
        layout.PHONE_W, layout.PHONE_H,
    )
    fill(c, layout.COLOR)
    draw_string(
        c, layout.BANNER_LEAD_X, layout.BANNER_LEAD_Y,
        texts.BANNER_LEAD, layout.FONT_H, layout.SIZE_BANNER,
    )
    draw_string(
        c, layout.BANNER_PHONE_X, layout.BANNER_PHONE_Y,
        texts.BANNER_PHONE, layout.FONT_HB, layout.SIZE_BANNER,
    )
    draw_string(
        c, layout.BANNER_NOTE_X, layout.BANNER_NOTE_Y,
        texts.BANNER_NOTE, layout.FONT_H, layout.SIZE_BANNER,
    )
    fill_subpaths(c, (vectors.TOP_RULE,), layout.COLOR_RULE_TOP)
