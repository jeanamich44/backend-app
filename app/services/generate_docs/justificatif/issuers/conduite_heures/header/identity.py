"""Nom de l'élève."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_identity:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.NAME_X, layout.NAME_Y,
        doc.card.eleve, layout.FONT_BOLD, layout.SIZE_NAME,
        max_width=layout.FILL_XS[-1] - layout.NAME_X,
    )
