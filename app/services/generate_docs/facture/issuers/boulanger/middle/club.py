from .. import copy, layout
from ..paint import escape_pdf

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    if not getattr(doc.visible, "middle", True):
        return False
    return bool(getattr(doc.visible, "middle_club", False))

# ----------------------------------------------------------------------

def get_lines(doc) -> list[str]:
    if not is_visible(doc):
        return []

    card = doc.card
    nom = getattr(card, "club_nom", copy.CLUB_NOM)
    if not nom:
        return []

    code = getattr(card, "club_code", copy.CLUB_CODE)
    qty = getattr(card, "club_qte", copy.CLUB_QTE)
    pu = getattr(card, "club_pu_ttc", copy.CLUB_PU_TTC)
    tva = getattr(card, "club_tva_taux", copy.CLUB_TVA_TAUX)
    tot = getattr(card, "club_total_ttc", copy.CLUB_TOTAL_TTC)

    pad = " " * layout.PAD_COLUMNS
    line_str = (
        f"{nom:<{layout.COL_DESC}}"
        f"{code:>{layout.COL_CODE}}"
        f"{qty:>{layout.COL_QTY}}"
        f"{pu:>{layout.COL_PU}}"
        f"{tva:>{layout.COL_TVA}}"
        f"{tot:>{layout.COL_TOTAL}}"
    )
    return [f"() '({pad}{escape_pdf(line_str)}) '"]

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
