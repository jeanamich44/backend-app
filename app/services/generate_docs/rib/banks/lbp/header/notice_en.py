"""Mention confidentialité EN (wrap + justification)."""

from .. import layout
from ..paint import draw_paragraph


def draw(c, doc):
    if not doc.visible.header_notice_en:
        return
    text = doc.header.notice_en
    if not text:
        return
    draw_paragraph(
        c,
        layout.MARGIN_LEFT,
        layout.NOTICE_EN_Y,
        text,
        layout.NOTICE_FONT,
        layout.NOTICE_SIZE,
        layout.NOTICE_LEADING,
        layout.CONTENT_W,
        layout.NOTICE_COLOR,
    )
