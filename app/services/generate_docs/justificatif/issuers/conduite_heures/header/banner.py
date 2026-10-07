"""Titre, avis d'annulation, date d'édition."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_banner:
        return
    fill(c, layout.COLOR_MUTED)
    edition = texts.EDITION_PREFIX + (doc.card.edition or "")
    draw_string(
        c, layout.EDITION_X, layout.EDITION_Y,
        edition, layout.FONT_TREBUCHET, layout.SIZE_EDITION,
    )
