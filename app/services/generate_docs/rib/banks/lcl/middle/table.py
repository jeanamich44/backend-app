"""Tableau national : 5 colonnes centrées, Verdana-Bold 7."""

from .. import copy as texts
from .. import layout
from ..paint import draw_centered, draw_string, fill


def draw(c, doc, i=0):
    if not doc.visible.middle_table:
        return
    d_title = layout.dy(i)
    d_grid = layout.dy_nat(i)
    fill(c, layout.NAVY)
    draw_string(
        c, layout.NAT_TITLE_X, layout.NAT_TITLE_Y + d_title, texts.NAT_TITLE,
        layout.FONT, layout.SECTION_SIZE,
        max_width=layout.NOTICE_W,
    )
    fill(c, layout.COLOR)
    cols = list(zip(
        layout.NAT_COLS,
        (
            texts.COL_BANQUE, texts.COL_GUICHET, texts.COL_COMPTE,
            texts.COL_CLE, texts.COL_DOM,
        ),
        (
            doc.card.banque, doc.card.guichet, doc.card.compte,
            doc.card.cle, doc.card.domiciliation,
        ),
    ))
    if not doc.visible.middle_domiciliation:
        cols = cols[:4]
    for col, ((x0, x1), label, value) in enumerate(cols):
        draw_string(
            c, layout.NAT_HEAD_X[col], layout.NAT_HEAD_Y + d_grid, label,
            layout.FONT_BOLD, layout.SIZE_FIELD,
            max_width=x1 - layout.NAT_HEAD_X[col],
        )
        if value:
            draw_centered(
                c, x0, x1, layout.NAT_VAL_Y + d_grid, value,
                layout.FONT_BOLD, layout.SIZE_FIELD,
            )
