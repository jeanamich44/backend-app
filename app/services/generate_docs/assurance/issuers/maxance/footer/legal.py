"""Logos pied de page (mentions via static.spans)."""

from .. import layout
from ..paint import draw_chrome


def draw(c, doc):
    draw_chrome(
        c, layout.EQUITY_FILE,
        layout.EQUITY_X, layout.EQUITY_Y,
        layout.EQUITY_W, layout.EQUITY_H,
    )
    draw_chrome(
        c, layout.ORIAS_FILE,
        layout.ORIAS_X, layout.ORIAS_Y,
        layout.ORIAS_W, layout.ORIAS_H,
    )
