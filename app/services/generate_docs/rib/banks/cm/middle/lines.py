"""Cadre et filets 1 pt noirs (traits iText, un seul passage)."""

from .. import layout
from ..paint import stroke_line, stroke_vline


def draw(c, doc, dy=0):
    if not doc.visible.middle_lines:
        return
    w = layout.LINE_WIDTH
    col = layout.LINE_COLOR
    x0, x1 = layout.BOX_X0, layout.BOX_X1
    y0, y1 = layout.BOX_Y0 + dy, layout.BOX_Y1 + dy
    stroke_line(c, x0, y0, x1, w, col)
    stroke_line(c, x0, y1, x1, w, col)
    stroke_vline(c, layout.BOX_VX0, y0, y1, w, col)
    stroke_vline(c, layout.BOX_VX1, y0, y1, w, col)
    left0, left1 = layout.TABLE_COLS[0][0], layout.TABLE_COLS[-1][1]
    stroke_line(c, left0, layout.TABLE_RULE_Y + dy, left1, w, col)
    stroke_line(c, layout.RIGHT_X0, layout.TABLE_RULE_Y + dy, layout.RIGHT_X1, w, col)
    stroke_line(c, left0, layout.IBAN_RULE_Y + dy, left1, w, col)
    stroke_line(c, layout.RIGHT_X0, layout.IBAN_RULE_Y + dy, layout.RIGHT_X1, w, col)
