"""Tableau articles : header PDF4NET, lignes, Envoi."""

from .. import copy as texts
from .. import layout, rules
from ..paint import (
    draw_kerned_html, fill, html_center_x, html_frame, wrap_kerned,
)
from .cell import draw_cell


def _edges(col_i, top=None, bottom=None):
    return {
        "left_outer": col_i == 0,
        "right_outer": col_i == len(layout.COL_W) - 1,
        "top": top,
        "bottom": bottom,
    }


def _cell(c, col_i, cm_y, height, **edges):
    c.saveState()
    c.translate(layout.COL_X[col_i] + 0.5, cm_y)
    draw_cell(c, layout.COL_W[col_i], height, layout.COLOR, **_edges(col_i, **edges))
    return c


def _close(c):
    c.restoreState()


def _label(c, col_i, tm_y, text, bold=False, center=False):
    font = layout.FONT_BOLD if bold else layout.FONT
    size = layout.SIZE_BODY
    x = 0
    if center:
        x = html_center_x(layout.COL_W[col_i], text, font, size)
    draw_kerned_html(c, x, tm_y, text, font, size)


def _header(c):
    h = layout.HEADER_LOCAL_H
    y = -0.5
    for col_i in range(8):
        _cell(c, col_i, y, h, top="full", bottom="full")
        fill(c, layout.COLOR)
        if col_i == 0:
            _label(c, col_i, layout.TM_Y_HEAD + 2 * layout.LINE, texts.COL_SKU, True)
        elif col_i == 1:
            _label(c, col_i, layout.TM_Y_HEAD + 2 * layout.LINE, texts.COL_DESC, True)
        elif col_i == 2:
            _label(c, col_i, layout.TM_Y_HEAD + layout.LINE, texts.COL_QTY, True, True)
            _label(c, col_i, layout.TM_Y_HEAD + 2 * layout.LINE, texts.COL_SHIPPED, True, True)
        elif col_i == 3:
            _label(c, col_i, layout.TM_Y_HEAD + layout.LINE, texts.COL_UNIT, True, True)
            _label(c, col_i, layout.TM_Y_HEAD + 2 * layout.LINE, texts.COL_GROSS, True, True)
        elif col_i == 4:
            _label(c, col_i, layout.TM_Y_HEAD + 2 * layout.LINE, texts.COL_DISC, True, True)
        elif col_i == 5:
            _label(c, col_i, layout.TM_Y_HEAD, texts.COL_PRICE, True, True)
            _label(c, col_i, layout.TM_Y_HEAD + layout.LINE, texts.COL_UNIT_2, True, True)
            _label(c, col_i, layout.TM_Y_HEAD + 2 * layout.LINE, texts.COL_NET, True, True)
        elif col_i == 6:
            _label(c, col_i, layout.TM_Y_HEAD + 2 * layout.LINE, texts.COL_TOTAL, True, True)
        else:
            _label(c, col_i, layout.TM_Y_HEAD + 2 * layout.LINE, texts.COL_VAT, True, True)
        _close(c)
    return y + layout.HEADER_H


def _row_band(c, cm_y, height, top=None, bottom=None):
    for col_i in range(8):
        _cell(c, col_i, cm_y, height, top=top, bottom=bottom)
        _close(c)


def _desc_lines(item):
    max_w = layout.COL_W[1] - 1.0
    lines = wrap_kerned(
        item.desc, layout.FONT, layout.SIZE_BODY, max_w, layout.MAX_DESC_LINES,
    )
    return lines or [""]


def _item(c, item, cm_y, first):
    lines = _desc_lines(item)
    n = max(1, len(lines))
    height = n * layout.LINE + (1.0 if first else 0.0)
    top = "join" if first else None
    base = layout.TM_Y_HEAD if first else layout.TM_Y
    last_y = base + (n - 1) * layout.LINE
    qte, brut, remise, ht_unit, line_ttc, _line_ht, tva_pct = rules.line_amounts(item)
    for col_i in range(8):
        _cell(c, col_i, cm_y, height, top=top)
        fill(c, layout.COLOR)
        if col_i == 0:
            _label(c, col_i, base, item.sku)
        elif col_i == 1:
            for i, line in enumerate(lines):
                _label(c, col_i, base + i * layout.LINE, line)
        elif col_i == 2:
            _label(c, col_i, last_y, rules.format_qty(qte), center=True)
        elif col_i == 3:
            _label(c, col_i, last_y, rules.format_euro(brut), center=True)
        elif col_i == 4:
            if remise:
                _label(c, col_i, last_y, rules.format_euro(remise), center=True)
        elif col_i == 5:
            _label(c, col_i, last_y, rules.format_euro(ht_unit), center=True)
        elif col_i == 6:
            _label(c, col_i, last_y, rules.format_euro(line_ttc), center=True)
        else:
            _label(c, col_i, last_y, rules.format_tva(tva_pct), center=True)
        _close(c)
    return cm_y + height


def _ship(c, cm_y):
    _row_band(c, cm_y, layout.LINE)
    cm_y += layout.LINE
    height = layout.LINE + 1.0
    qte = rules.parse_qty(texts.SHIP_QTE)
    for col_i in range(8):
        _cell(c, col_i, cm_y, height, bottom="last")
        fill(c, layout.COLOR)
        if col_i == 1:
            _label(c, col_i, layout.TM_Y, texts.SHIP_LABEL)
        elif col_i == 2:
            _label(c, col_i, layout.TM_Y, rules.format_qty_int(qte), center=True)
        elif col_i in (3, 5, 6):
            _label(c, col_i, layout.TM_Y, rules.format_euro(0), center=True)
        elif col_i == 7:
            _label(c, col_i, layout.TM_Y, rules.format_tva(layout.TVA_RATE), center=True)
        _close(c)
    return cm_y + height


def draw(c, doc):
    c.saveState()
    html_frame(c, layout.TABLE_X, layout.TABLE_Y)
    cm_y = -0.5
    if doc.visible.middle_columns:
        cm_y = _header(c)
    else:
        cm_y = -0.5 + layout.HEADER_H
    if doc.visible.middle_rows:
        items = doc.card.items[: layout.MAX_ROWS]
        for i, item in enumerate(items):
            cm_y = _item(c, item, cm_y, first=(i == 0))
            _row_band(c, cm_y, layout.LINE)
            cm_y += layout.LINE
        _ship(c, cm_y)
    c.restoreState()
