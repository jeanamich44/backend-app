"""Mentions légales myPOS Ltd + folio + filet bas."""

from .. import copy as texts
from .. import layout
from ..paint import draw_right, draw_string, fill_rgb, stroke_line


def draw(c, doc):
    if not doc.visible.footer:
        return
    fill_rgb(c, layout.COLOR)
    if doc.visible.footer_legal:
        draw_string(
            c, layout.LEFT_X, layout.FOOTER_YS[0], texts.FOOTER_1,
            layout.FONT, layout.SIZE_FOOTER,
        )
        draw_string(
            c, layout.LEFT_X, layout.FOOTER_YS[1], texts.FOOTER_2,
            layout.FONT, layout.SIZE_FOOTER,
        )
    if doc.visible.footer_page and doc.footer.page:
        draw_right(
            c, layout.RIGHT_X, layout.PAGE_NO_Y,
            f"  {doc.footer.page}",
            layout.FONT_BOLD, layout.SIZE_BODY,
        )
    stroke_line(
        c, layout.RIGHT_X, layout.LEFT_X, layout.BOT_LINE_Y,
        layout.HEAD_LINE_W, layout.COLOR_BAR, cap=0,
    )
