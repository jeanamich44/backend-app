"""Commande / facture / N/Réf / matricule."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_order:
        return
    card = doc.card
    web = rules.en_ligne(card)
    fill(c, layout.COLOR)
    if web:
        x = layout.ORDER_X
        draw_string(
            c, x, layout.ORDER_CMD_Y_WEB,
            f"{texts.CMD_WEB} {card.num_commande}",
            layout.FONT_BOLD, layout.SIZE_11, max_width=250,
        )
        draw_string(
            c, x, layout.ORDER_CMD_DATE_Y_WEB,
            f"{texts.DU_WEB} {card.date_commande}",
            layout.FONT_BOLD, layout.SIZE_9, max_width=250,
        )
        draw_string(
            c, x, layout.ORDER_INV_Y_WEB,
            f"{texts.INV_WEB} {card.num_facture}",
            layout.FONT_BOLD, layout.SIZE_11, max_width=250,
        )
        draw_string(
            c, x, layout.ORDER_INV_DATE_Y_WEB,
            f"{texts.DU_WEB} {card.date_facture}",
            layout.FONT_BOLD, layout.SIZE_9, max_width=250,
        )
    else:
        x = layout.ORDER_X_MAG
        draw_string(
            c, x, layout.ORDER_CMD_Y_MAG,
            f"{texts.CMD_MAG} {card.num_commande}",
            layout.FONT_BOLD, layout.SIZE_11, max_width=280,
        )
        draw_string(
            c, x, layout.ORDER_CMD_DATE_Y_MAG,
            f"{texts.DU_MAG} {card.date_commande}",
            layout.FONT, layout.SIZE_11, max_width=280,
        )
        draw_string(
            c, x, layout.ORDER_INV_Y_MAG,
            f"{texts.INV_MAG} {card.num_facture}",
            layout.FONT_BOLD, layout.SIZE_11, max_width=280,
        )
        draw_string(
            c, x, layout.ORDER_INV_DATE_Y_MAG,
            f"{texts.DU_MAG} {card.date_facture}",
            layout.FONT, layout.SIZE_11, max_width=280,
        )
        mat = (card.matricule or "").strip()
        if mat:
            draw_string(
                c, x, layout.ORDER_MAT_Y_MAG,
                f"{texts.MAT_LABEL} {mat}",
                layout.FONT, layout.SIZE_11, max_width=280,
            )
    nref = (card.nref or "").strip()
    if nref:
        draw_string(
            c, layout.NREF_X, layout.NREF_Y,
            texts.NREF_PREFIX + nref,
            layout.FONT, layout.SIZE_7, max_width=300,
        )
