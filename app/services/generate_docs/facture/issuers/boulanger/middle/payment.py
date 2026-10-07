from .. import layout
from ..paint import escape_pdf

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    return bool(getattr(doc.visible, "middle_payment", True) and getattr(doc.visible, "middle", True))

# ----------------------------------------------------------------------

def get_lines(doc) -> list[str]:
    if not is_visible(doc):
        return []

    card = doc.card
    pad = " " * layout.PAD_COLUMNS
    mode_str = getattr(card, "reglement_mode", "Carte Bancaire")
    montant_str = getattr(card, "reglement_montant", card.total_ttc)

    pay = f"{'REGLEMENTS':<30}{mode_str:<40}{montant_str:>10}"

    return [
        "() '",
        f"()({pad}{escape_pdf(pay)}) '",
    ]

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
