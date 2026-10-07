from reportlab.pdfbase.pdfmetrics import stringWidth
from .. import layout
from ..paint import draw_string, fill

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.header_meta:
        return

    items = (
        (doc.header.label_commande, doc.header.val_commande, layout.META_CMD_VAL_X, layout.META_ROW_YS[0]),
        (doc.header.label_facture, doc.header.val_facture, layout.META_FAC_VAL_X, layout.META_ROW_YS[1]),
        (doc.header.label_date, doc.header.val_date, layout.META_DATE_VAL_X, layout.META_ROW_YS[2]),
    )

    for label, val, default_val_x, y in items:
        if label:
            fill(c, layout.COLOR_BLACK)
            draw_string(
                c,
                layout.META_LABEL_X,
                y,
                label,
                layout.FONT_BOLD,
                layout.FONT_SIZE_BODY,
            )
        if val:
            fill(c, layout.COLOR_GREY)
            val_x = default_val_x
            if label:
                calc_x = layout.META_LABEL_X + stringWidth(label, layout.FONT_BOLD, layout.FONT_SIZE_BODY) + 2.5
                if abs(calc_x - default_val_x) > 10.0:
                    val_x = calc_x
            draw_string(
                c,
                val_x,
                y,
                val,
                layout.FONT_REGULAR,
                layout.FONT_SIZE_BODY,
            )
