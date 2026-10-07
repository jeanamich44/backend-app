"""Pagination Page n/n Fin (coin des encadrés adresses)."""

from .. import copy as texts
from .. import layout, rules
from ..paint import clip_rect, draw_string, fill, stroke, y_up


def draw(c, doc, plan):
    if not doc.visible.header_page:
        return
    fill(c, layout.COLOR)
    text = texts.PAGE_FMT.format(current=plan.index + 1, total=plan.count)
    web = rules.en_ligne(doc.card)
    if web:
        x0, y0, x1, y1 = layout.PAGE_CLIP
        x, y = layout.PAGE_X, layout.PAGE_Y
        for _ in range(2):
            c.saveState()
            clip_rect(c, x0, y0, x1, y1)
            draw_string(c, x, y, text, layout.FONT, layout.SIZE_7)
            c.restoreState()
        return
    x0, y0, x1, y1 = layout.PAGE_CLIP_MAG
    c.saveState()
    clip_rect(c, x0, y0, x1, y1)
    stroke(c, layout.COLOR)
    c.setLineWidth(layout.PAGE_STROKE_MAG)
    t = c.beginText()
    t.setTextRenderMode(2)
    t.setFont(layout.FONT, layout.SIZE_7)
    t.setCharSpace(layout.PAGE_TC_MAG)
    t.setTextOrigin(layout.PAGE_X_MAG, y_up(layout.PAGE_Y_MAG))
    t.textOut(text)
    c.drawText(t)
    c.restoreState()
