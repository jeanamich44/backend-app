"""Deux rangées de tirets : un fill par rangée, chemins du gabarit (pas des re)."""

from .. import layout
from ..paint import fill_dash_row


def draw(c, doc):
    if not doc.visible.middle_lines:
        return
    for y0 in layout.DASH_YS:
        fill_dash_row(
            c, y0, y0 + layout.DASH_H,
            layout.DASH_W, layout.DASH_STEP, layout.DASH_COUNT,
            layout.DASH_COLOR,
        )
