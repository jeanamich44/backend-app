"""Grille du tableau (U / pointillés du gabarit) + cadre footer."""

from .. import layout
from ..paint import fill_rect, stroke_line, stroke_path, stroke_re, stroke_u


def _header(c):
    xs = layout.FILL_XS
    y0, y1 = layout.HEAD_FILL_Y
    yt, yb = layout.HEAD_U_Y
    for i, (x_l, x_r) in enumerate(layout.HEAD_U):
        fill_rect(c, xs[i], y0, xs[i + 1], y1, layout.COLOR_WHITE)
        stroke_u(c, x_l, x_r, yt, yb, layout.GRID_W, layout.COLOR_GRID)
    fill_rect(c, xs[4], y0, xs[5], y1, layout.COLOR_WHITE)
    stroke_re(c, *layout.HEAD_LAST_RE, layout.GRID_W, layout.COLOR_GRID)


def _data_row(c, index: int):
    y0, y_re, y_line = layout.data_stroke_ys(index)
    ox0, ox1 = layout.DATA_OUTER
    stroke_re(c, ox0, y0, ox1, y_re, layout.GRID_W, layout.COLOR_GRID)
    fy0, fy1 = layout.data_fill_ys(index)
    xs = layout.FILL_XS
    for col, (x_l, x_r, dash_side) in enumerate(layout.DATA_CELLS):
        fill_rect(c, xs[col], fy0, xs[col + 1], fy1, layout.COLOR_WHITE)
        stroke_line(c, x_l, y0, x_r, y0, layout.GRID_W, layout.COLOR_GRID)
        right_dash = layout.GRID_DASH if dash_side == "right" else None
        stroke_line(
            c, x_r, y0, x_r, y_line,
            layout.GRID_W, layout.COLOR_GRID, dash=right_dash,
        )
        stroke_line(c, x_l, y_line, x_r, y_line, layout.GRID_W, layout.COLOR_GRID)
        left_dash = layout.GRID_DASH if dash_side == "left" else None
        stroke_line(
            c, x_l, y0, x_l, y_line,
            layout.GRID_W, layout.COLOR_GRID, dash=left_dash,
        )


def _table(c, n_rows: int):
    _header(c)
    for i in range(n_rows):
        _data_row(c, i)


def _footer_frame(c):
    x0, y0, x1, y1 = layout.FOOTER_FILL
    fill_rect(c, x0, y0, x1, y1, layout.COLOR_WHITE)
    stroke_path(
        c, layout.FOOTER_PATH,
        layout.FOOTER_STROKE_W, layout.COLOR_GRID, cap=0,
    )


def draw(c, doc):
    if doc.visible.middle:
        n = min(len(doc.card.rdvs), layout.MAX_ROWS)
        _table(c, n)
    if doc.visible.footer:
        _footer_frame(c)
