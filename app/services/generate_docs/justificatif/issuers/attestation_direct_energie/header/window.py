"""Fenêtre destinataire : M. + NOM / rue / CP VILLE en capitales."""

from .. import layout, rules
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_window:
        return
    fill(c, layout.COLOR)
    for y, line in zip(layout.WIN_Y, rules.window_lines(doc.card)):
        draw_string(
            c, layout.WIN_X, y, line,
            layout.FONT, layout.WIN_SIZE,
            max_width=layout.WIN_MAX_W,
        )
