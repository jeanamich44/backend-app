"""Filet bas (Canva G6 : LW 2, cap round)."""

from .. import layout
from ..paint import stroke_line


def draw(c, doc):
    if not doc.visible.footer_line:
        return
    stroke_line(
        c, layout.FOOT_RULE_X0, layout.FOOT_RULE_Y,
        layout.FOOT_RULE_X1, layout.FOOT_RULE_Y,
        layout.FOOT_RULE_W, layout.COLOR, cap=1,
    )
