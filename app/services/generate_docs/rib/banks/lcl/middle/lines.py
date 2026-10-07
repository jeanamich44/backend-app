"""Cadres biseau : carte + grilles nationale / internationale."""

from .. import layout
from ..paint import bevel_box


def draw(c, doc, i=0):
    if not doc.visible.middle_lines:
        return
    d_nat = layout.dy_nat(i)
    d_intl = layout.dy(i)
    # Coupon 3 : haut −0.5 (Skia), bas à ×221 — sinon la boîte est trop courte.
    bevel_box(
        c, *layout.BOX_OUTER, layout.BEVEL_OUTER,
        layout.dy_c3(i), dy1=layout.dy(i),
    )
    bevel_box(c, *layout.BOX_NAT, layout.BEVEL_INNER, d_nat)
    bevel_box(c, *layout.BOX_INTL, layout.BEVEL_INNER, d_intl)
    hy0, hy1 = layout.NAT_HEAD_BOX_Y
    vy0, vy1 = layout.NAT_VAL_BOX_Y
    nat_cols = layout.NAT_COLS
    if not doc.visible.middle_domiciliation:
        nat_cols = nat_cols[:4]
    for x0, x1 in nat_cols:
        bevel_box(c, x0, hy0, x1, hy1, layout.BEVEL_INNER, d_nat)
        bevel_box(c, x0, vy0, x1, vy1, layout.BEVEL_INNER, d_nat)
    hy0, hy1 = layout.INTL_HEAD_BOX_Y
    vy0, vy1 = layout.INTL_VAL_BOX_Y
    for x0, x1 in layout.INTL_COLS:
        bevel_box(c, x0, hy0, x1, hy1, layout.BEVEL_INNER, d_intl)
        bevel_box(c, x0, vy0, x1, vy1, layout.BEVEL_INNER, d_intl)
