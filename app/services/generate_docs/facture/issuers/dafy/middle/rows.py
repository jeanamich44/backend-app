from .. import copy as texts
from .. import layout, rules
from ..paint import draw_center, draw_string, fill, fill_ops, width
from . import vectors


def _attr_line(c, x, y, label, value):
    draw_string(
        c, x, y, label, layout.FONT_BOLD, layout.SIZE_BODY,
        max_width=layout.ATTR_MAX_W,
    )
    suffix = texts.ATTR_SEP + value
    left = x + width(label, layout.FONT_BOLD, layout.SIZE_BODY)
    rest = layout.ATTR_MAX_W - (left - x)
    if rest > 2:
        draw_string(c, left, y, suffix, layout.FONT, layout.SIZE_BODY, max_width=rest)


def draw(c, doc):
    if not doc.visible.middle_rows:
        return
    bands = layout.row_bands(doc.card.items, layout.addr_shift(doc.card))
    fill(c, layout.COLOR)
    size = layout.SIZE_BODY
    for y_top, y_bot, item in bands:
        for ops in vectors.row_ops(y_top, y_bot):
            fill_ops(c, ops, layout.COLOR_GRAY)
        ny = layout.num_y(y_top, y_bot)
        qte, pu, cost = rules.line_cost(item)
        rate = rules.line_tva_rate(item)
        dy = y_top + layout.DESC_FROM_TOP
        if item.desc:
            draw_string(
                c, layout.DESC_X, dy, item.desc,
                layout.FONT_BOLD, size, max_width=layout.DESC_MAX_W,
            )
        if (item.couleur or "").strip():
            dy += layout.LINE_PITCH
            _attr_line(c, layout.DESC_X, dy, texts.ATTR_COULEUR, item.couleur)
        if (item.taille or "").strip():
            dy += layout.LINE_PITCH
            _attr_line(c, layout.DESC_X, dy, texts.ATTR_TAILLE, item.taille)
        if item.sku:
            draw_center(c, layout.REF_CX, ny, item.sku, layout.FONT, size)
        if item.qte:
            draw_center(
                c, layout.QTY_CX, ny, rules.format_qty(qte), layout.FONT, size,
            )
        if item.pu:
            draw_center(
                c, layout.PU_CX, ny, rules.format_euro(pu), layout.FONT, size,
            )
        if item.tva or item.pu:
            draw_center(
                c, layout.TVA_CX, ny, rules.format_tva_line(rate),
                layout.FONT, size,
            )
        if item.qte or item.pu:
            draw_center(
                c, layout.MNT_CX, ny, rules.format_euro(cost), layout.FONT, size,
            )
