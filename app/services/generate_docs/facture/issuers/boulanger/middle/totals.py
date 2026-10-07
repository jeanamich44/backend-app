from .. import layout
from ..paint import escape_pdf

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    return bool(getattr(doc.visible, "middle_totals", True) and getattr(doc.visible, "middle", True))

# ----------------------------------------------------------------------

def get_lines(doc) -> list[str]:
    if not is_visible(doc):
        return []

    card = doc.card
    pad_tot = " " * layout.PAD_TOTALS

    t0 = escape_pdf(f"{'TOTAL HT (Euros)':<{layout.COL_TOTALS_LABEL}}{card.total_ht:>{layout.COL_TOTALS_AMOUNT}}")
    t1 = escape_pdf(f"{'TOTAL TTC (Euros)':<{layout.COL_TOTALS_LABEL}}{card.total_ttc:>{layout.COL_TOTALS_AMOUNT}}")
    tva_lbl = f"Dont TVA ({card.dont_tva_taux}%)"
    t2 = escape_pdf(f"{tva_lbl:<{layout.COL_TOTALS_LABEL}}{card.dont_tva:>{layout.COL_TOTALS_AMOUNT}}")
    t3 = escape_pdf(f"{'Dont \xe9co-part. DEEE (TTC)':<{layout.COL_TOTALS_LABEL}}{card.dont_ecopart:>{layout.COL_TOTALS_AMOUNT}}")

    return [
        f"() '({pad_tot}{t0}) '",
        f"({pad_tot}{t1}) '",
        f"({pad_tot}{t2}) '",
        f"({pad_tot}{t3}) '",
    ]

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
