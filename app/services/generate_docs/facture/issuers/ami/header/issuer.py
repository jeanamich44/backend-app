"""Bloc émetteur (nom, téléphone, adresse AMI)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_issuer:
        return
    rows = (
        (layout.ISSUER_X[0], layout.ISSUER_Y[0], texts.ISSUER_NOM, layout.COLOR_MUTED),
        (layout.ISSUER_X[1], layout.ISSUER_Y[1], texts.PHONE, layout.COLOR_MUTED),
        (layout.ISSUER_X[2], layout.ISSUER_Y[2], texts.ISSUER_ADDR, layout.COLOR),
    )
    for x, y, text, color in rows:
        fill(c, color)
        draw_string(c, x, y, text, layout.FONT, layout.SIZE_ISSUER)
