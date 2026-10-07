from .. import copy, layout
from ..paint import escape_pdf

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    return bool(getattr(doc.visible, "footer_company", True) and getattr(doc.visible, "footer", True))

# ----------------------------------------------------------------------

def get_lines(doc) -> list[str]:
    if not is_visible(doc):
        return []

    card = doc.card
    seller_type = getattr(card, "seller_type", copy.SELLER_BOULANGER)
    pad = " " * layout.PAD_COLUMNS

    if seller_type == copy.SELLER_TIERS:
        v_nom = getattr(card, "seller_name", copy.TIERS_VENDEUR_NOM)
        v_cap = getattr(card, "seller_capital", copy.TIERS_VENDEUR_CAPITAL)
        v_rue = getattr(card, "seller_rue", copy.TIERS_VENDEUR_RUE)
        v_rcs = getattr(card, "seller_rcs", copy.TIERS_VENDEUR_RCS)
        v_cp = getattr(card, "seller_cp_ville", copy.TIERS_VENDEUR_CP_VILLE)
        v_tva = getattr(card, "seller_tva", copy.TIERS_VENDEUR_TVA)

        cp1 = escape_pdf(f"{v_nom:<{layout.LEFT_COLUMN_WIDTH}}Au capital de {v_cap}")
        cp2 = escape_pdf(f"{v_rue:<{layout.LEFT_COLUMN_WIDTH}}{v_rcs}")
        cp3 = escape_pdf(f"{v_cp:<{layout.LEFT_COLUMN_WIDTH}}TVA I.C. {v_tva}")
        cp4 = escape_pdf(f"Facture \xe9mise par Boulanger SA au nom et pour le compte de {v_nom}")

        return [
            f"({pad}{cp1}) '",
            f"({pad}{cp2}) '",
            f"({pad}{cp3}) '",
            f"({pad}{cp4}) '",
        ]
    else:
        c_nom = getattr(card, "company_nom", copy.COMPANY_NOM)
        c_cap = getattr(card, "company_capital", copy.COMPANY_CAPITAL)
        c_rue = getattr(card, "company_rue", copy.COMPANY_RUE)
        c_rcs = getattr(card, "company_rcs", copy.COMPANY_RCS)
        c_ville = getattr(card, "company_cp_ville", copy.COMPANY_CP_VILLE)
        c_tva = getattr(card, "company_tva", copy.COMPANY_TVA)
        c_ape = getattr(card, "company_ape", copy.COMPANY_APE)

        cp1 = escape_pdf(f"{c_nom:<{layout.LEFT_COLUMN_WIDTH}}{c_cap}")
        cp2 = escape_pdf(f"{c_rue:<{layout.LEFT_COLUMN_WIDTH}}{c_rcs}")
        cp3 = escape_pdf(f"{c_ville:<{layout.LEFT_COLUMN_WIDTH}}{c_tva}")
        cp4 = escape_pdf(f"{'':<{layout.LEFT_COLUMN_WIDTH}}{c_ape}")

        return [
            f"({pad}{cp1}) '",
            f"({pad}{cp2}) '",
            f"({pad}{cp3}) '",
            f"({pad}{cp4}) '",
        ]

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
