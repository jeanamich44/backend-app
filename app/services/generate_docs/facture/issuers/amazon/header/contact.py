"""Lien service client (chrome émetteur)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string


def draw(c, doc):
    if not doc.visible.header_contact:
        return
    draw_string(
        c, layout.CONTACT_X, layout.CONTACT_Y,
        texts.CONTACT, layout.FONT_UNI, layout.SIZE_SMALL,
        color=layout.COLOR,
    )
    draw_string(
        c, layout.CONTACT_URL_X, layout.CONTACT_Y,
        texts.CONTACT_URL, layout.FONT_UNI, layout.SIZE_SMALL,
        color=layout.COLOR_LINK,
    )
