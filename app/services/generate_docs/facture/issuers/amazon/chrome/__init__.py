"""Chrome : barre supérieure + encadré Payé (modèle amazon2/3)."""

from .. import layout
from ..paint import fill_rect


def draw_bar(c):
    x0, x1 = layout.BAR_X
    fill_rect(c, x0, 0, x1, layout.BAR_Y1, layout.COLOR_BAR)


def draw_pay_box(c):
    x0, y0, x1, y1 = layout.PAY_BOX
    t = layout.PAY_FRAME
    fill_rect(c, x0, y0, x1, y1, layout.COLOR_PAY)
    fill_rect(c, x0, y0, x1, y0 + t, layout.COLOR_PAY_BORDER)
    fill_rect(c, x0, y0, x0 + t, y1, layout.COLOR_PAY_BORDER)
    fill_rect(c, x0, y1 - t, x1, y1, layout.COLOR_PAY_BORDER)
    fill_rect(c, x1 - t, y0, x1, y1, layout.COLOR_PAY_BORDER)
    rx0, ry0, rx1, ry1 = layout.PAY_RULE
    fill_rect(c, rx0, ry0, rx1, ry1, layout.COLOR_LINE)


def draw(c, doc, plan):
    if not doc.visible.header:
        return
    draw_bar(c)
    if plan.kind == "full" and doc.visible.header_pay:
        draw_pay_box(c)
