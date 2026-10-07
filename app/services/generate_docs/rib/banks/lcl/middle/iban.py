"""IBAN : titre section + cellule gauche."""

from .. import copy as texts
from .. import layout
from .. import rib
from ..paint import draw_centered, draw_string, fill


def draw(c, doc, i=0):
    vis = doc.visible
    if not vis.middle_iban and not vis.middle_bic:
        return
    fill(c, layout.NAVY)
    draw_string(
        c, layout.INTL_TITLE_X, layout.INTL_TITLE_Y + layout.dy_nat(i), texts.INTL_TITLE,
        layout.FONT, layout.SECTION_SIZE,
        max_width=layout.NOTICE_W,
    )
    if not vis.middle_iban:
        return
    d = layout.dy(i)
    fill(c, layout.COLOR)
    x0, x1 = layout.INTL_COLS[0]
    draw_string(
        c, layout.INTL_HEAD_X[0], layout.INTL_HEAD_Y + d, texts.LABEL_IBAN,
        layout.FONT_BOLD, layout.SIZE_FIELD,
        max_width=x1 - layout.INTL_HEAD_X[0],
    )
    if doc.card.iban:
        draw_centered(
            c, x0, x1, layout.INTL_VAL_Y + d,
            rib.format_groups(doc.card.iban, 4),
            layout.FONT_BOLD, layout.SIZE_FIELD,
        )
