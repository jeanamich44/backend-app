"""Nom du compte : Regular 7.5 gris, TJ du gabarit sur le préfixe."""

from .. import copy as texts
from .. import glyphs
from .. import layout
from ..paint import draw_glyphs, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_account:
        return
    name = doc.card.account_name
    if not name:
        return
    fill(c, layout.COLOR_GRAY)
    if texts.ACCOUNT_PREFIX == "Nom du compte : ":
        draw_glyphs(
            c, layout.ACCOUNT_Y, glyphs.NOM_PREFIX,
            layout.FONT, layout.SIZE_ACCOUNT,
        )
        draw_string(
            c, glyphs.NOM_VALUE_X, layout.ACCOUNT_Y, name,
            layout.FONT, layout.SIZE_ACCOUNT,
            max_width=layout.ACCOUNT_W - (glyphs.NOM_VALUE_X - layout.LEFT_X),
        )
    else:
        draw_string(
            c, layout.LEFT_X, layout.ACCOUNT_Y,
            texts.ACCOUNT_PREFIX + name,
            layout.FONT, layout.SIZE_ACCOUNT,
            max_width=layout.ACCOUNT_W,
        )
