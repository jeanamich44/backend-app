"""Lignes article + éco-participation."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_center, draw_right, draw_string, fill


def _line(c, item, index: int, fallback_date: str):
    y = layout.row_at(layout.ROW_Y, index)
    y2 = layout.row_at(layout.ROW_Y2, index)
    pieces_y = layout.row_at(layout.ROW_PIECES_Y, index)
    rate_y = layout.row_at(layout.TVA_RATE_Y, index)
    ht, vat, ttc = rules.line_amounts(item)
    date = item.date_delivrance or fallback_date
    if item.sku:
        draw_string(
            c, layout.SKU_X, y, item.sku, layout.FONT, layout.SIZE_ROW,
        )
    if item.qte:
        draw_center(
            c, layout.QTY_CX, y, item.qte, layout.FONT, layout.SIZE_ROW,
        )
    if item.desc:
        draw_string(
            c, layout.LIB_X, y, item.desc, layout.FONT, layout.SIZE_ROW,
            max_width=layout.ROW_MAX_W,
        )
    if item.desc2:
        draw_string(
            c, layout.LIB_X, y2, item.desc2,
            layout.FONT, layout.SIZE_ROW, max_width=layout.ROW_MAX_W,
        )
    draw_string(
        c, layout.LIB_X, pieces_y, texts.PIECES,
        layout.FONT, layout.SIZE_PIECES, max_width=layout.ROW_MAX_W,
    )
    if date:
        draw_string(
            c, layout.DATE_DELIV_X, y, date,
            layout.FONT, layout.SIZE_ROW,
        )
    draw_right(
        c, layout.HT_RIGHT, y, rules.format_eur(ht),
        layout.FONT, layout.SIZE_ROW,
    )
    draw_right(
        c, layout.TVA_AMT_RIGHT, y, rules.format_money(vat),
        layout.FONT, layout.SIZE_ROW,
    )
    draw_right(
        c, layout.TVA_AMT_RIGHT, rate_y,
        rules.format_pct(rules.parse_money(item.tva)),
        layout.FONT, layout.SIZE_PIECES,
    )
    draw_right(
        c, layout.TTC_RIGHT, y, rules.format_eur(ttc),
        layout.FONT, layout.SIZE_ROW,
    )


def _eco(c, dy: float, rate: float):
    y = layout.ECO_Y + dy
    rate_y = layout.ECO_RATE_Y + dy
    draw_string(
        c, layout.LIB_X, y, texts.ECO,
        layout.FONT, layout.SIZE_ROW,
    )
    draw_right(
        c, layout.HT_RIGHT, y, rules.format_eur(0),
        layout.FONT, layout.SIZE_ROW,
    )
    draw_right(
        c, layout.TVA_AMT_RIGHT, y, rules.format_money(0),
        layout.FONT, layout.SIZE_ROW,
    )
    draw_right(
        c, layout.TVA_AMT_RIGHT, rate_y,
        rules.format_pct(rate),
        layout.FONT, layout.SIZE_PIECES,
    )
    draw_right(
        c, layout.ECO_TTC_RIGHT, y, rules.format_eur(0),
        layout.FONT, layout.SIZE_ROW,
    )


def draw(c, doc):
    if not doc.visible.middle_rows:
        return
    items = list(doc.card.items or ())[: layout.MAX_ROWS]
    fill(c, layout.COLOR)
    fallback_date = items[0].date_delivrance if items else ""
    for i, item in enumerate(items):
        _line(c, item, i, fallback_date)
    rate = rules.parse_money(items[0].tva) if items else 0.0
    _eco(c, layout.table_shift(doc.card), rate)
