"""Filet bas G7 (LW 2), cloné en Y si extra lignes."""

from .. import layout
from ..chrome import vectors
from ..paint import stroke_seg


def draw(c, doc):
    if not doc.visible.middle_line:
        return
    dy = layout.table_shift(doc.card)
    stroke_seg(
        c, layout.shift_line(vectors.FOOT_LINE, dy),
        layout.RULE_W_FOOT, layout.COLOR,
    )
