"""Lignes article : textes. Vecteurs = columns (ordre flux)."""

from .. import layout, rules
from ..paint import draw_string, fill, wrap_text


def _cell(c, x, y, text, max_w):
    if not text:
        return
    draw_string(
        c, x, y, rules.cell(text),
        layout.FONT, layout.SIZE_BODY,
        max_width=max_w,
    )


def draw(c, doc):
    if not doc.visible.middle_rows:
        return
    items = list(doc.card.items or ())[: layout.MAX_ROWS]
    if not items:
        return
    fill(c, layout.COLOR)
    for i, item in enumerate(items):
        y = layout.row_text_y(i)
        qte, pu, ht, _vat = rules.line_amounts(item)
        rate = rules.parse_money(item.tva)
        _cell(c, layout.SKU_X, y, item.sku, layout.SKU_MAX_W)
        lines = wrap_text(
            item.desc, layout.FONT, layout.SIZE_BODY, layout.DESC_MAX_W, 3,
        )
        for j, line in enumerate(lines):
            text = rules.cell(line) if j == 0 else line
            draw_string(
                c, layout.DESC_X, y + j * layout.ROW_LINE_PITCH,
                text, layout.FONT, layout.SIZE_BODY,
                max_width=layout.DESC_MAX_W,
            )
        _cell(c, layout.TAX_X, y, rules.format_pct(rate), layout.CELL_MAX_W)
        _cell(c, layout.BASE_X, y, rules.format_eur(pu), layout.CELL_MAX_W)
        _cell(c, layout.PU_X, y, rules.format_eur(pu), layout.CELL_MAX_W)
        _cell(c, layout.QTY_X, y, rules.format_qty(qte), layout.QTY_MAX_W)
        _cell(c, layout.LINE_HT_X, y, rules.format_eur(ht), layout.CELL_MAX_W)
