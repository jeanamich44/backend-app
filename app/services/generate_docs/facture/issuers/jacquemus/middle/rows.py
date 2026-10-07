from .. import layout
from ..paint import draw_line, draw_string, fill

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle_rows:
        return
    items = doc.middle.items[:layout.MAX_ROWS]
    for i, item in enumerate(items):
        y_shift = i * layout.ROW_H
        fill(c, layout.COLOR_BLACK)
        draw_string(c, layout.ITEM_NOM_X, layout.ITEM_NOM_Y + y_shift, item.nom, layout.FONT_BOLD, layout.FONT_SIZE_BODY)

        fill(c, layout.COLOR_GREY)
        ref_str = f"REF : {item.ref}" if item.ref else "REF : "
        draw_string(c, layout.ITEM_DETAIL_X, layout.ITEM_DETAIL_Y_START + y_shift, ref_str, layout.FONT_REGULAR, layout.FONT_SIZE_BODY)

        coul_str = f"Couleur: {item.couleur}" if item.couleur else "Couleur:"
        draw_string(c, layout.ITEM_DETAIL_X, layout.ITEM_DETAIL_Y_START + y_shift + layout.ITEM_DETAIL_LEADING, coul_str, layout.FONT_REGULAR, layout.FONT_SIZE_BODY)

        taille_str = f"Taille: {item.taille}" if item.taille else "Taille:"
        draw_string(c, layout.ITEM_DETAIL_X, layout.ITEM_DETAIL_Y_START + y_shift + 2 * layout.ITEM_DETAIL_LEADING, taille_str, layout.FONT_REGULAR, layout.FONT_SIZE_BODY)

        pays_str = f"Pays de fabrication: {item.pays}" if item.pays else "Pays de fabrication:"
        draw_string(c, layout.ITEM_DETAIL_X, layout.ITEM_DETAIL_Y_START + y_shift + 3 * layout.ITEM_DETAIL_LEADING, pays_str, layout.FONT_REGULAR, layout.FONT_SIZE_BODY)

        y_val = layout.ITEM_ROW_VAL_Y + y_shift
        fill(c, layout.COLOR_GREY)
        draw_string(c, layout.ITEM_PRIX_X, y_val, item.prix, layout.FONT_REGULAR, layout.FONT_SIZE_BODY)
        draw_string(c, layout.ITEM_QTE_X, y_val, str(item.qte), layout.FONT_REGULAR, layout.FONT_SIZE_BODY)

        fill(c, layout.COLOR_BLACK)
        draw_string(c, layout.ITEM_SOUS_TOTAL_X, y_val, item.sous_total or item.prix, layout.FONT_BOLD, layout.FONT_SIZE_BODY)

    n = max(1, len(items))
    y_bottom = layout.ROW_BOTTOM_LINE_Y + (n - 1) * layout.ROW_H
    draw_line(c, layout.ROW_BOTTOM_LINE_X1, y_bottom, layout.ROW_BOTTOM_LINE_X2, y_bottom, layout.LINE_WIDTH, layout.COLOR_BLACK, cap=1)
