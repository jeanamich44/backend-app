"""Mentions SumUp Limited, bas de page (gauche + droite)."""

from .. import layout
from ..paint import draw_right, draw_string, fill


def draw(c, doc):
    if not doc.visible.footer:
        return
    fill(c, layout.COLOR)
    font, size = layout.FONT, layout.SIZE_FOOTER
    if doc.visible.footer_legal and doc.footer.legal:
        y = layout.FOOTER_Y
        for line in doc.footer.legal.split("\n"):
            draw_string(c, layout.FOOTER_X, y, line, font, size)
            y += layout.FOOTER_LEADING
    if doc.visible.footer_legal_right and doc.footer.legal_right:
        y = layout.FOOTER_RIGHT_Y
        for line in doc.footer.legal_right.split("\n"):
            draw_right(c, layout.FOOTER_RIGHT_X, y, line, font, size)
            y += layout.FOOTER_LEADING
