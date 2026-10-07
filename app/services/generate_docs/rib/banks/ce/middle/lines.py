from .. import layout
from ..paint import stroke_line


def draw_iban_line(c, doc, dy=0):
    if not doc.visible.middle_lines:
        return
    stroke_line(
        c, layout.LINE_IBAN_X0, layout.LINE_IBAN_Y + dy, layout.LINE_IBAN_X1,
        layout.LINE_WIDTH, layout.LINE_COLOR,
    )


def draw_table_line(c, doc, dy=0):
    if not doc.visible.middle_lines:
        return
    stroke_line(
        c, layout.LINE_TABLE_X0, layout.LINE_TABLE_Y + dy, layout.LINE_TABLE_X1,
        layout.LINE_WIDTH, layout.LINE_COLOR,
    )


def draw_solids(c, doc, dy=0):
    draw_iban_line(c, doc, dy)
    draw_table_line(c, doc, dy)


def draw_separators(c, doc, dy=0):
    if not doc.visible.middle_lines:
        return
    stroke_line(
        c, layout.LINE_SEP_X0, layout.LINE_SEP_Y + dy, layout.LINE_SEP_X_MID,
        layout.LINE_SEP_WIDTH, layout.LINE_SEP_COLOR,
        dash=layout.LINE_SEP_DASH_LEFT,
    )
    stroke_line(
        c, layout.LINE_SEP_X_MID, layout.LINE_SEP_Y + dy, layout.LINE_SEP_X1,
        layout.LINE_SEP_WIDTH, layout.LINE_SEP_COLOR,
        dash=layout.LINE_SEP_DASH_RIGHT,
    )

