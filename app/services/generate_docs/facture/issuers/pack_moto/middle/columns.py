"""En-tête tableau articles : labels. Grille = draw_grid (ordre flux TCPDF)."""

from .. import layout
from ..paint import draw_string, fill, fill_rect, stroke_line, stroke_rect
from . import vectors


def draw_grid(c, n: int):
    extra = (max(1, n) - 1) * layout.ROW_H
    stroke_rect(
        c, *vectors.table_outer(extra),
        layout.STROKE_W, layout.COLOR, cap=layout.STROKE_CAP,
    )
    for i in range(max(1, n)):
        for rect in vectors.row_fills(i, layout.ROW_H):
            fill_rect(c, *rect, (1, 1, 1))
    for i in range(max(1, n)):
        y = vectors.row_hair_y(i, layout.ROW_H)
        for x0, x1 in vectors.HAIR_SEGS:
            stroke_line(
                c, x0, y, x1, y,
                layout.STROKE_W, layout.COLOR_HAIR, cap=layout.STROKE_CAP,
            )
    for rect in vectors.HEAD_FILLS:
        fill_rect(c, *rect, layout.COLOR_CELL)
    for x0, x1 in vectors.HAIR_SEGS:
        stroke_line(
            c, x0, vectors.HAIR_HEAD_Y, x1, vectors.HAIR_HEAD_Y,
            layout.STROKE_W, layout.COLOR, cap=layout.STROKE_CAP,
        )


def draw(c, doc):
    if not doc.visible.middle_columns:
        return
    fill(c, layout.COLOR)
    for x, y, label in layout.COL_LABELS:
        draw_string(c, x, y, label, layout.FONT_BOLD, layout.SIZE_BODY)
