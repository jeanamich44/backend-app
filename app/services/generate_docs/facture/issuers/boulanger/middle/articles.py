from .. import copy, layout
from ..paint import escape_pdf

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    return bool(getattr(doc.visible, "middle_articles", True) and getattr(doc.visible, "middle", True))

# ----------------------------------------------------------------------

def get_lines(doc) -> list[str]:
    if not is_visible(doc):
        return []

    card = doc.card
    pad = " " * layout.PAD_COLUMNS
    lines = []

    items = getattr(card, "items", [])[:layout.MAX_ITEMS]
    seller_type = getattr(card, "seller_type", copy.SELLER_BOULANGER)
    global_seller = getattr(card, "seller_name", copy.TIERS_VENDEUR_NOM)

    for item in items:
        desc = item.nom or ""
        code = item.code or ""
        qty = item.qte or "1"
        pu = item.pu_ttc or ""
        tva = item.tva_taux or "20,00"
        tot = item.total_ttc or pu

        main_str = (
            f"{desc:<{layout.COL_DESC}}"
            f"{code:>{layout.COL_CODE}}"
            f"{qty:>{layout.COL_QTY}}"
            f"{pu:>{layout.COL_PU}}"
            f"{tva:>{layout.COL_TVA}}"
            f"{tot:>{layout.COL_TOTAL}}"
        )
        lines.append(f"() '({pad}{escape_pdf(main_str)}) '")

        item_seller = getattr(item, "vendeur", None) or (global_seller if seller_type == copy.SELLER_TIERS else None)
        if item_seller and seller_type == copy.SELLER_TIERS:
            lines.append(f"({pad}{escape_pdf(f'Vendu et exp\xe9di\xe9 par {item_seller}')}) '")

        if getattr(item, "ecopart", None):
            eco_str = f"{'ECO-PART DEEE':<70}{item.ecopart:>10}"
            lines.append(f"({pad}{escape_pdf(eco_str)}) '")

        if getattr(item, "garantie_non_retenue", None):
            lines.append(f"({pad}{escape_pdf(item.garantie_non_retenue)}) '")

        if getattr(item, "garantie_reparation", None):
            lines.append(f"({pad}{escape_pdf(item.garantie_reparation)}) '")

        if getattr(item, "dispo_pieces", None):
            lbl = getattr(item, "dispo_pieces_label", None) or "Disponibilit\xe9 des pi\xe8ces d\xe9tach\xe9es (donn\xe9e fournisseur) :"
            lines.append(f"({pad}{escape_pdf(lbl)}) '")
            lines.append(f"({pad}{escape_pdf(item.dispo_pieces)}) '")

    extra_nom = getattr(card, "extra_line_nom", None)
    if extra_nom:
        e_code = getattr(card, "extra_line_code", "")
        e_qty = getattr(card, "extra_line_qte", "1")
        e_pu = getattr(card, "extra_line_pu_ttc", "0,00")
        e_tva = getattr(card, "extra_line_tva", "20,00")
        e_tot = getattr(card, "extra_line_total", e_pu)
        extra_str = (
            f"{extra_nom:<{layout.COL_DESC}}"
            f"{e_code:>{layout.COL_CODE}}"
            f"{e_qty:>{layout.COL_QTY}}"
            f"{e_pu:>{layout.COL_PU}}"
            f"{e_tva:>{layout.COL_TVA}}"
            f"{e_tot:>{layout.COL_TOTAL}}"
        )
        lines.append(f"() '({pad}{escape_pdf(extra_str)}) '")

    return lines

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
