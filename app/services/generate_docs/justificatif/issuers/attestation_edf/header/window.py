"""Adresse fenêtre (Courier-Bold, capitales)."""

from .. import layout, rules
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_window:
        return
    nom, adresse, ville = rules.window_lines(doc.card)
    fill(c, layout.COLOR_BLACK)
    draw_string(c, layout.WIN_X1, layout.WIN_Y[0], nom, layout.FONT_C, layout.WIN_SIZE)
    draw_string(c, layout.WIN_X, layout.WIN_Y[1], adresse, layout.FONT_C, layout.WIN_SIZE)
    draw_string(c, layout.WIN_X, layout.WIN_Y[2], ville, layout.FONT_C, layout.WIN_SIZE)
