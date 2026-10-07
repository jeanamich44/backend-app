"""Sincerely, nom, cœur AMI."""

from .. import copy as texts
from .. import layout
from ..paint import draw_chrome, draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_sign:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.THANKS_X, layout.SINCERE_Y,
        texts.SINCERELY, layout.FONT_FOOTER, layout.SIZE_FOOTER,
        max_width=layout.THANKS_MAX_W,
    )
    draw_string(
        c, layout.THANKS_X, layout.SIGN_NAME_Y,
        texts.SIGN_NAME, layout.FONT_FOOTER, layout.SIZE_FOOTER,
        max_width=layout.THANKS_MAX_W,
    )
    draw_chrome(
        c, layout.SIGN_FILE,
        layout.SIGN_X, layout.SIGN_Y,
        layout.SIGN_W, layout.SIGN_H,
    )
