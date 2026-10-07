"""Signature manuscrit + nom / fonction (chrome émetteur)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_image, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_sign:
        return
    draw_image(
        c, layout.SIGN_FILE,
        layout.SIGN_X, layout.SIGN_Y,
        layout.SIGN_W, layout.SIGN_H,
    )
    fill(c, layout.COLOR)
    draw_string(
        c, layout.SIGN_NAME_X, layout.SIGN_NAME_Y,
        texts.SIGN_NAME, layout.FONT, layout.SIGN_SIZE,
    )
    draw_string(
        c, layout.SIGN_ROLE_X, layout.SIGN_ROLE_Y,
        texts.SIGN_ROLE, layout.FONT, layout.SIGN_SIZE,
    )
