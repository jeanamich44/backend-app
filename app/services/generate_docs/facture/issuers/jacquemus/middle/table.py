from .. import layout
from ..paint import draw_line, draw_string, fill

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle_table:
        return
    fill(c, layout.COLOR_BLACK)
    draw_string(c, layout.COL_PRODUITS_X, layout.COL_HEAD_Y, doc.middle.col_produits, layout.FONT_BOLD, layout.FONT_SIZE_BODY)
    draw_string(c, layout.COL_PRIX_X, layout.COL_HEAD_Y, doc.middle.col_prix, layout.FONT_BOLD, layout.FONT_SIZE_BODY)
    draw_string(c, layout.COL_QTE_X, layout.COL_HEAD_QTE_Y, doc.middle.col_qte, layout.FONT_BOLD, layout.FONT_SIZE_BODY)
    draw_string(c, layout.COL_SOUS_TOTAL_X, layout.COL_HEAD_Y, doc.middle.col_sous_total, layout.FONT_BOLD, layout.FONT_SIZE_BODY)
    draw_line(c, layout.TABLE_LINE_X1, layout.TABLE_LINE_Y, layout.TABLE_LINE_X2, layout.TABLE_LINE_Y, layout.LINE_WIDTH, layout.COLOR_BLACK, cap=1)
