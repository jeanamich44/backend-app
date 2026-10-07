"""Sections 6–8 : icônes téléphone + signature (textes via static.spans)."""

from .. import layout
from ..paint import draw_chrome


def draw(c, doc):
    draw_chrome(
        c, layout.PHONE_ICON,
        layout.PHONE_ICON_X1, layout.PHONE_ICON_Y,
        layout.PHONE_ICON_W, layout.PHONE_ICON_H,
    )
    draw_chrome(
        c, layout.PHONE_ICON,
        layout.PHONE_ICON_X2, layout.PHONE_ICON_Y,
        layout.PHONE_ICON_W, layout.PHONE_ICON_H,
    )
    draw_chrome(
        c, layout.MAP_FILE,
        layout.MAP_X, layout.MAP_Y,
        layout.MAP_W, layout.MAP_H,
    )
