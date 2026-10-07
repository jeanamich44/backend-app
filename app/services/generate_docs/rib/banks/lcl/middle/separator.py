"""Filet de séparation entre coupons : tirets 1.5 / 1.005 du gabarit."""

from .. import layout
from ..paint import dashed_rule


def draw(c, doc, i=0):
    dashed_rule(
        c,
        layout.SEP_X0,
        layout.SEP_X1,
        layout.SEP_Y + layout.dy(i),
        layout.SEP_H,
        layout.SEP_DASH_ON,
        layout.SEP_DASH_GAP,
        layout.COLOR,
        clip_x1=layout.SEP_CLIP_X1,
    )
