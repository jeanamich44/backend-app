"""Bloc magasin / entrepôt à gauche."""

from .. import flow, layout, rules
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_store:
        return
    web = rules.en_ligne(doc.card)
    lines = flow.store_lines(doc.card)
    if not lines:
        return
    fill(c, layout.COLOR)
    if web:
        x, y, pitch = layout.STORE_X, layout.STORE_Y0_WEB, layout.STORE_PITCH_WEB
        font = layout.FONT_BOLD
    else:
        x, y, pitch = layout.STORE_X_MAG, layout.STORE_Y0_MAG, layout.STORE_PITCH_MAG
        font = layout.FONT_BOLD
    for i, line in enumerate(lines):
        use = font if web or i == 0 else layout.FONT
        draw_string(c, x, y + i * pitch, line, use, layout.SIZE_11, max_width=290)
