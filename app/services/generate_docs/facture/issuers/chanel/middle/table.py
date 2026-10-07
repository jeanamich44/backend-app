from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle_table:
        return
    paint.draw_text(c, layout.COL_REF_X, layout.TABLE_HEADER_Y, doc.middle.col_ref_title, layout.FONT_BOLD, layout.MIDDLE_SIZE)
    paint.draw_text(c, layout.COL_QTE_X, layout.TABLE_HEADER_Y, doc.middle.col_qte_title, layout.FONT_BOLD, layout.MIDDLE_SIZE)
    paint.draw_right_text(c, layout.COL_PU_RIGHT, layout.TABLE_HEADER_Y, doc.middle.col_pu_title, layout.FONT_BOLD, layout.MIDDLE_SIZE)
    paint.draw_right_text(c, layout.COL_MONTANT_RIGHT, layout.TABLE_HEADER_Y, doc.middle.col_montant_title, layout.FONT_BOLD, layout.MIDDLE_SIZE)

    items = getattr(doc.middle, "items", None) or []
    items = items[:3]
    if not items:
        return

    row_step = 28.0
    for i, it in enumerate(items):
        y_desc = layout.ARTICLE_DESC_Y - i * row_step
        y_ref = layout.ARTICLE_REF_Y - i * row_step
        y_qte = layout.COL_QTE_Y - i * row_step
        y_pu = layout.COL_PU_Y - i * row_step
        y_montant = layout.COL_MONTANT_Y - i * row_step

        if it.desc:
            paint.draw_text(c, layout.ARTICLE_DESC_X, y_desc, it.desc, layout.FONT_BOLD, layout.MIDDLE_SIZE)
        if it.ref:
            paint.draw_text(c, layout.ARTICLE_REF_X, y_ref, it.ref, layout.FONT_REGULAR, layout.MIDDLE_SIZE)
        if it.qty:
            paint.draw_right_text(c, layout.COL_QTE_RIGHT, y_qte, it.qty, layout.FONT_REGULAR, layout.MIDDLE_SIZE)
        if it.unit_price:
            paint.draw_right_text(c, layout.COL_PU_RIGHT, y_pu, it.unit_price, layout.FONT_REGULAR, layout.MIDDLE_SIZE)
        if it.total:
            paint.draw_right_text(c, layout.COL_MONTANT_RIGHT, y_montant, it.total, layout.FONT_REGULAR, layout.MIDDLE_SIZE)

    if len(items) <= 2:
        count_y = layout.COUNT_Y
    else:
        count_y = 394.0

    if doc.middle.articles_count:
        paint.draw_center_text(c, layout.COUNT_CENTER_X, count_y, doc.middle.articles_count, layout.FONT_BOLD, layout.MIDDLE_SIZE)

