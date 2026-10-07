from .. import layout, paint

# ----------------------------------------------------------------------

def _split_desc(text: str, max_chars: int = 36) -> tuple[str, str]:
    text = (text or "").strip()
    if "\n" in text:
        parts = text.split("\n", 1)
        return parts[0].strip(), parts[1].strip()
    if len(text) <= max_chars:
        return text, ""
    split_pos = text.rfind(" ", 0, max_chars)
    if split_pos == -1:
        split_pos = max_chars
    line1 = text[:split_pos].strip()
    line2 = text[split_pos:].strip()
    return line1, line2

# ----------------------------------------------------------------------

def draw(c, doc) -> float:
    paint.draw_text(c, layout.COL_REF_TITLE_X, layout.COL_REF_TITLE_Y, "Référence article", layout.FONT_REGULAR, 9.01, layout.COLOR_GREY, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.COL_TVA_TITLE_X, layout.COL_TVA_TITLE_Y, "Taux TVA %", layout.FONT_REGULAR, 9.01, layout.COLOR_GREY, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.COL_QTY_TITLE_X, layout.COL_QTY_TITLE_Y, "Quantité", layout.FONT_REGULAR, 9.01, layout.COLOR_GREY, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.COL_PRICE_TITLE_X, layout.COL_PRICE_TITLE_Y, "Prix Unit.", layout.FONT_REGULAR, 9.01, layout.COLOR_GREY)
    paint.draw_text(c, layout.COL_PRICE_SUB_X, layout.COL_PRICE_SUB_Y, "Brut HT", layout.FONT_REGULAR, 9.01, layout.COLOR_GREY)
    paint.draw_text(c, layout.COL_REMISE_TITLE_X, layout.COL_REMISE_TITLE_Y, "Montant", layout.FONT_REGULAR, 9.01, layout.COLOR_GREY)
    paint.draw_text(c, layout.COL_REMISE_SUB_X, layout.COL_REMISE_SUB_Y, "Remise HT", layout.FONT_REGULAR, 9.01, layout.COLOR_GREY)
    paint.draw_text(c, layout.COL_NET_TITLE_X, layout.COL_NET_TITLE_Y, "Montant", layout.FONT_REGULAR, 9.01, layout.COLOR_GREY)
    paint.draw_text(c, layout.COL_NET_SUB_X, layout.COL_NET_SUB_Y, "Net HT", layout.FONT_REGULAR, 9.01, layout.COLOR_GREY)

    paint.draw_line(c, 40.75, layout.TABLE_LINE_D4_Y, 579.71, layout.TABLE_LINE_D4_Y, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)

    items = doc.card.items or []
    current_y = 417.48

    for idx, item in enumerate(items):
        ref_text = item.ref.strip() if item.ref else ""
        if ref_text and not ref_text.endswith(" "):
            ref_text += " "
        paint.draw_text(c, layout.ITEM_REF_X, current_y + 1.16, ref_text, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)

        desc1, desc2 = _split_desc(item.desc)
        if desc1:
            paint.draw_text(c, layout.ITEM_DESC_X, current_y + 0.10, desc1, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_DESC)
        if desc2:
            paint.draw_text(c, layout.ITEM_DESC_X, current_y + 13.46, desc2, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_DESC)

        val_y = current_y + 6.57
        if item.tva_rate:
            paint.draw_text(c, layout.ITEM_TVA_X, val_y, item.tva_rate, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
        if item.qty:
            paint.draw_text(c, layout.ITEM_QTY_X, val_y, item.qty, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
        if item.unit_price:
            paint.draw_text(c, layout.ITEM_PRICE_X, val_y + 0.19, item.unit_price, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
        if item.remise:
            paint.draw_text(c, layout.ITEM_REMISE_X, val_y + 0.19, item.remise, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
        if item.net_ht:
            paint.draw_text(c, layout.ITEM_NET_X, val_y + 0.19, item.net_ht, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)

        dash_y = current_y + 17.89
        c.saveState()
        c.setStrokeColor(paint.to_color(layout.COLOR_LINE))
        c.setLineWidth(layout.LINE_WIDTH)
        c.setDash([0.75, 0.75], 0)
        c.line(258.66, paint.y_up(dash_y), 579.42, paint.y_up(dash_y))
        c.restoreState()

        if item.remise_code:
            promo_y = current_y + 29.67
            paint.draw_text(c, layout.ITEM_REMISE_CODE_X, promo_y, item.remise_code, layout.FONT_ITALIC, 9.01, layout.COLOR_GREY)
            current_y += 38.0
        else:
            current_y += 26.0

    final_d6_y = max(454.26, current_y - 1.22)
    paint.draw_line(c, 40.75, final_d6_y, 579.71, final_d6_y, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)

    return final_d6_y - 454.26
