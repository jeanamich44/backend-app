"""Lignes article : TVA, EAN, ref, qté, libellé, extras, volume, montants."""

from .. import copy as texts
from .. import flow, layout, rules
from ..paint import draw_money, draw_string, fill, width


def _amount(c, web, euro_x, right, y, value):
    gap = None if web else width(" ", layout.FONT, layout.SIZE_8)
    draw_money(
        c, euro_x, y, rules.format_money(value),
        layout.FONT, layout.SIZE_8,
        layout.EURO_W_8, layout.EURO_ABOVE_8, layout.EURO_BELOW_8,
        gap=gap,
    )


def _eco_mag(c, y, eco_ht, eco_ttc):
    for x, val in (
        (layout.ECO_HT_X, eco_ht),
        (layout.ECO_TTC_X, eco_ttc),
        (layout.ECO_MT_X, eco_ht),
    ):
        num = rules.format_money(val) + " "
        draw_string(c, x, y, num, layout.FONT, layout.SIZE_8)
        draw_string(
            c, x + width(num, layout.FONT, layout.SIZE_8), y,
            "€", layout.FONT, layout.SIZE_8,
        )


def draw(c, doc, plan):
    if not doc.visible.middle_rows:
        return
    web = rules.en_ligne(doc.card)
    y = layout.ITEM_Y0
    desc_x = layout.DESC_X if web else layout.DESC_X_MAG
    fill(c, layout.COLOR)
    for item in plan.items:
        qte, ht, ttc, line_ht, _line_ttc = rules.line_amounts(item)
        code = (doc.card.tva_code or "").strip() or ("I" if web else "1")
        draw_string(c, layout.TVA_X, y, code, layout.FONT, layout.SIZE_8)
        draw_string(c, layout.EAN_X, y, item.ean, layout.FONT, layout.SIZE_8, max_width=58)
        draw_string(c, layout.REF_X, y, item.reference, layout.FONT, layout.SIZE_8, max_width=32)
        draw_string(c, layout.QTE_X, y, rules.format_qty(qte), layout.FONT, layout.SIZE_8)
        titles = flow.title_lines(item)
        first = titles[0] if titles else ""
        title_size = layout.SIZE_8 if web else layout.SIZE_8_5
        desc_y = y + layout.DESC_DY
        draw_string(
            c, desc_x, desc_y, first, layout.FONT, title_size,
            max_width=layout.DESC_RIGHT - desc_x,
        )
        _amount(c, web, layout.HT_EURO_X, layout.HT_RIGHT, y, ht)
        _amount(c, web, layout.TTC_EURO_X, layout.TTC_RIGHT, y, ttc)
        _amount(c, web, layout.MT_EURO_X, layout.MT_RIGHT, y, line_ht)
        cursor = desc_y
        for extra_title in titles[1:]:
            cursor += layout.TITLE_PITCH
            draw_string(
                c, desc_x, cursor, extra_title, layout.FONT, title_size,
                max_width=layout.DESC_RIGHT - desc_x,
            )
        extras = flow.extra_lines(item, web)
        for extra in extras:
            kind = extra[3]
            cursor += layout.REMISE_PITCH if kind == "remise" else layout.EXTRA_PITCH
            draw_string(
                c, desc_x, cursor, extra[0], layout.FONT, extra[1],
                max_width=layout.DESC_RIGHT - desc_x,
            )
            if kind == "eco":
                eco_ht, eco_ttc = extra[4], extra[5]
                if web:
                    _amount(c, web, layout.HT_EURO_X, layout.HT_RIGHT, cursor, eco_ht)
                    _amount(c, web, layout.TTC_EURO_X, layout.TTC_RIGHT, cursor, eco_ttc)
                    _amount(c, web, layout.MT_EURO_X, layout.MT_RIGHT, cursor, eco_ht)
                else:
                    _eco_mag(c, cursor, eco_ht, eco_ttc)
        vol_y = cursor + (layout.VOLUME_GAP_WEB if web else layout.VOLUME_GAP_MAG)
        vol_size = layout.SIZE_8 if web else layout.SIZE_8_5
        qty_font = layout.FONT_BOLD if web else layout.FONT
        draw_string(
            c, layout.QTE_X, vol_y, rules.format_qty(qte),
            qty_font, vol_size,
        )
        draw_string(
            c, desc_x, vol_y, texts.VOLUME,
            layout.FONT_BOLD, vol_size,
        )
        y += flow.item_height(item, web)
