from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if doc.visible.header_facturation:
        paint.draw_line(
            c,
            layout.FACTURATION_LINE_X,
            layout.FACTURATION_LINE_Y1,
            layout.FACTURATION_LINE_X,
            layout.FACTURATION_LINE_Y2,
            width=layout.LINE_MAGENTA_WIDTH,
            color=layout.COLOR_MAGENTA,
        )
        if doc.card.facturation_titre:
            paint.draw_text(
                c,
                layout.FACTURATION_TITLE_X,
                layout.FACTURATION_TITLE_Y,
                doc.card.facturation_titre,
                layout.FONT_REGULAR,
                layout.FACTURATION_TITLE_SIZE,
                layout.COLOR_MAGENTA,
                char_space=layout.CHAR_SPACE_FACTURATION,
            )
        lines_fac = [
            doc.card.client_nom,
            doc.card.client_rue,
            doc.card.client_ville,
            doc.card.client_pays,
        ]
        for i, text in enumerate(lines_fac):
            if text:
                y = layout.FACTURATION_TEXT_Y + (i * layout.FACTURATION_TEXT_LEADING)
                paint.draw_text(
                    c,
                    layout.FACTURATION_TEXT_X,
                    y,
                    text,
                    layout.FONT_SANS,
                    layout.FACTURATION_TEXT_SIZE,
                    layout.COLOR_MAGENTA,
                    char_space=layout.CHAR_SPACE_SANS,
                )

    if doc.visible.header_livraison:
        paint.draw_line(
            c,
            layout.LIVRAISON_LINE_X,
            layout.LIVRAISON_LINE_Y1,
            layout.LIVRAISON_LINE_X,
            layout.LIVRAISON_LINE_Y2,
            width=layout.LINE_MAGENTA_WIDTH,
            color=layout.COLOR_MAGENTA,
        )
        if doc.card.livraison_titre:
            paint.draw_text(
                c,
                layout.LIVRAISON_TITLE_X,
                layout.LIVRAISON_TITLE_Y,
                doc.card.livraison_titre,
                layout.FONT_REGULAR,
                layout.LIVRAISON_TITLE_SIZE,
                layout.COLOR_MAGENTA,
                char_space=layout.CHAR_SPACE_FACTURATION,
            )
        lines_liv = [
            doc.card.livraison_nom,
            doc.card.livraison_rue,
            doc.card.livraison_ville,
            doc.card.livraison_pays,
        ]
        for i, text in enumerate(lines_liv):
            if text:
                y = layout.LIVRAISON_TEXT_Y + (i * layout.LIVRAISON_TEXT_LEADING)
                paint.draw_text(
                    c,
                    layout.LIVRAISON_TEXT_X,
                    y,
                    text,
                    layout.FONT_SANS,
                    layout.LIVRAISON_TEXT_SIZE,
                    layout.COLOR_MAGENTA,
                    char_space=layout.CHAR_SPACE_SANS,
                )
