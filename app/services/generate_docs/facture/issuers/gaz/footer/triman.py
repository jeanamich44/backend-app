"""Triman + info-tri, gauche du bandeau contacts."""

from .. import layout
from ..chrome.triman_paths import TRIMAN_PARTS
from ..paint import draw_string_rot90, fill, fill_ops


def draw(c, doc):
    if not doc.visible.footer_triman:
        return
    for color, even_odd, ops in TRIMAN_PARTS:
        fill_ops(c, ops, color, even_odd=even_odd)
    fill(c, layout.COLOR_WHITE)
    for y, ch in zip(layout.FR_Y, "FR"):
        draw_string_rot90(
            c, layout.FR_X, y, ch,
            layout.FONT_VERDANA_BOLD, layout.SIZE_FR,
        )
