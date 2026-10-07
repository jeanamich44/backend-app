"""Carte SWIFT : round rect #EBEBE8, pastille, notice Regular 6.75."""

from .. import copy as texts
from .. import glyphs
from .. import layout
from ..paint import draw_glyphs, draw_string, fill, fill_fills
from ..header.paths import SWIFT_BADGE, SWIFT_BOX


def draw(c, doc):
    if not doc.visible.middle_swift:
        return
    fill_fills(c, (SWIFT_BOX,), layout.SWIFT_BOX_COLOR)
    fill_fills(c, (SWIFT_BADGE,), layout.COLOR)
    fill(c, layout.COLOR_WHITE)
    draw_glyphs(
        c, layout.SWIFT_BADGE_Y, glyphs.SWIFT_BADGE,
        layout.FONT_BOLD, layout.SIZE_BADGE,
    )
    fill(c, layout.COLOR_GRAY)
    draw_glyphs(c, layout.SWIFT_YS[0], glyphs.SWIFT_L1, layout.FONT, layout.SIZE_SWIFT)
    draw_glyphs(c, layout.SWIFT_YS[1], glyphs.SWIFT_L2, layout.FONT, layout.SIZE_SWIFT)
    draw_glyphs(c, layout.SWIFT_YS[2], glyphs.SWIFT_L3A, layout.FONT, layout.SIZE_SWIFT)
    draw_glyphs(c, layout.SWIFT_YS[2], glyphs.SWIFT_L3B, layout.FONT, layout.SIZE_SWIFT)
    y = layout.SWIFT_YS[3]
    if texts.SWIFT_L4_CODE == "TRWIBEB3XXX":
        draw_glyphs(c, y, glyphs.SWIFT_L4_PRE, layout.FONT, layout.SIZE_SWIFT)
        draw_glyphs(c, y, glyphs.SWIFT_L4_CODE, layout.FONT_BOLD, layout.SIZE_SWIFT)
        draw_glyphs(c, y, glyphs.SWIFT_L4_DOT, layout.FONT, layout.SIZE_SWIFT)
    else:
        xs = layout.SWIFT_L4_XS
        draw_string(c, xs[0], y, "SWIFT", layout.FONT, layout.SIZE_SWIFT)
        draw_string(c, xs[1], y, " : ", layout.FONT, layout.SIZE_SWIFT, char_space=-0.0002)
        draw_string(c, xs[2], y, texts.SWIFT_L4_CODE, layout.FONT_BOLD, layout.SIZE_SWIFT)
        draw_string(c, xs[4], y, texts.SWIFT_L4_DOT, layout.FONT, layout.SIZE_SWIFT)
