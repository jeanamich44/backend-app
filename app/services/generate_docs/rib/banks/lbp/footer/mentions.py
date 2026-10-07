"""Pied de page : mentions LBP + code document."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_mentions:
        return
    foot = doc.footer
    fill(c, layout.FOOTER_COLOR)
    if foot.line1:
        draw_string(
            c, layout.FOOTER_X, layout.FOOTER_Y1, foot.line1,
            layout.FOOTER_FONT, layout.FOOTER_SIZE,
        )
    if foot.line2:
        draw_string(
            c, layout.FOOTER_X, layout.FOOTER_Y2, foot.line2,
            layout.FOOTER_FONT, layout.FOOTER_SIZE,
        )
    if foot.code:
        draw_string(
            c, layout.FOOTER_CODE_X, layout.FOOTER_CODE_Y, foot.code,
            layout.FOOTER_CODE_FONT, layout.FOOTER_CODE_SIZE,
        )
