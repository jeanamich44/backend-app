"""Chrome : cadres adresses, tableau, TVA/paiement, aide, bande commande, code-barres."""

from .. import barcode, layout, rules
from ..paint import channel_green, fill_rect, fill_stroke_rect, stroke_line, stroke_rect


def _table(c):
    x0, y0, x1, y1 = layout.TABLE
    head = layout.TABLE_HEAD_Y1
    fill_rect(c, x0, y0, x1, head, channel_green(c))
    stroke_line(c, x0, head, x1, head, layout.STROKE_FAT, layout.COLOR)
    stroke_line(c, x0, y0, x0, y1, layout.STROKE_FAT, layout.COLOR)
    stroke_line(c, x0, y0, x1, y0, layout.STROKE_FAT, layout.COLOR)
    stroke_line(c, x1, y0, x1, y1, layout.STROKE_FAT, layout.COLOR)
    for x in layout.COLS[1:-1]:
        stroke_line(c, x, y0, x, y1, layout.STROKE_THIN, layout.COLOR)


def _addresses(c):
    x0, x1 = layout.ADDR_X0, layout.ADDR_X1
    stroke_rect(
        c, x0, layout.ADDR_LIV_Y0, x1, layout.ADDR_LIV_Y1,
        layout.STROKE_THIN, layout.COLOR,
    )
    stroke_rect(
        c, x0, layout.ADDR_FAC_Y0, x1, layout.ADDR_FAC_Y1,
        layout.STROKE_THIN, layout.COLOR,
    )


def _vat_pay(c):
    vx0, vy0, vx1, vy1 = layout.VAT_BOX
    hx0, hy0, hx1, hy1 = layout.VAT_HEAD
    px0, py0, px1, py1 = layout.PAY_HEAD
    fill_rect(c, hx0, hy0, hx1, hy1, channel_green(c))
    fill_rect(c, px0, py0, px1, py1, channel_green(c))
    for x in layout.VAT_COLS[1:-1]:
        stroke_line(c, x, vy0, x, vy1, layout.STROKE_THIN, layout.COLOR)
    pay0, pay1, split = layout.PAY_X0, layout.PAY_X1, layout.PAY_SPLIT_Y
    stroke_line(c, pay0, vy0, pay0, split, layout.STROKE_THIN, layout.COLOR)
    stroke_line(c, pay1, vy0, pay1, split, layout.STROKE_THIN, layout.COLOR)
    stroke_line(c, pay0, split, pay0, vy1, layout.STROKE_THIN, layout.COLOR)
    stroke_line(c, pay0, split, pay1, split, layout.STROKE_THIN, layout.COLOR)
    stroke_line(c, pay1, split, pay1, vy1, layout.STROKE_THIN, layout.COLOR)
    stroke_line(c, pay0, vy1, pay1, vy1, layout.STROKE_THIN, layout.COLOR)
    stroke_line(c, vx0, vy0, vx0, vy1, layout.STROKE_FAT, layout.COLOR)
    stroke_line(c, vx1, vy0, vx1, vy1, layout.STROKE_FAT, layout.COLOR)
    stroke_line(c, vx0, vy1, vx1, vy1, layout.STROKE_FAT, layout.COLOR)


def _help_box_web(c, x0, y0, x1, y1, line_w):
    stroke_line(c, x0, y0, x0, y1, line_w, layout.COLOR)
    stroke_line(c, x0, y0, x1, y0, line_w, layout.COLOR)
    stroke_line(c, x1, y0, x1, y1, line_w, layout.COLOR)
    stroke_line(c, x0, y1, x1, y1, line_w, layout.COLOR)


def _help(c, web: bool):
    line_w = layout.STROKE_THIN
    if web:
        x0, y0, x1, y1 = layout.HELP
        px0, py0, px1, py1 = layout.PILL
    else:
        x0, y0, x1, y1 = layout.HELP_MAG
        px0, py0, px1, py1 = layout.PILL_MAG
    _help_box_web(c, x0, y0, x1, y1, line_w)
    fill_stroke_rect(
        c, px0, py0, px1, py1,
        layout.COLOR_WHITE, layout.COLOR, line_w,
    )
    _help_box_web(c, px0, py0, px1, py1, line_w)


def _order_band(c, web: bool):
    if not web:
        return
    x0, y0, x1, y1 = layout.ORDER_BAND
    fill_rect(c, x0, y0, x1, y1, layout.COLOR_GRAY)


def _barcode(c, doc):
    web = rules.en_ligne(doc.card)
    box = layout.BARCODE_WEB if web else layout.BARCODE_MAG
    barcode.draw(c, rules.barcode_value(doc.card), box)


def _shown(doc, *names):
    vis = doc.visible
    return all(getattr(vis, name) for name in names)


def draw(c, doc, plan):
    if _shown(doc, "header", "header_addresses"):
        _addresses(c)
    if _shown(doc, "header", "header_order"):
        _order_band(c, plan.footer_kind == rules.FOOTER_WEB)
        _barcode(c, doc)
    if _shown(doc, "middle") and (
        doc.visible.middle_columns or doc.visible.middle_rows
    ):
        _table(c)
    if _shown(doc, "middle", "middle_vat"):
        _vat_pay(c)
    if _shown(doc, "footer", "footer_help"):
        _help(c, plan.footer_kind == rules.FOOTER_WEB)
