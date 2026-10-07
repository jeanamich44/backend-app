"""Titre Certificat IBAN + cache blanc derrière (rect du gabarit)."""

from .. import layout
from ..paint import draw_string, fill_rect, fill_rgb, width


def draw(c, doc):
    if not doc.visible.header_title:
        return
    title = (doc.header.title or "") + layout.TITLE_PAD
    w = width(title, layout.FONT_BOLD, layout.SIZE_TITLE)
    if w:
        fill_rect(c, layout.TITLE_X, layout.TITLE_MASK_Y, w, layout.TITLE_MASK_H)
    fill_rgb(c, layout.COLOR)
    draw_string(
        c, layout.TITLE_X, layout.TITLE_Y, title,
        layout.FONT_BOLD, layout.SIZE_TITLE,
    )
