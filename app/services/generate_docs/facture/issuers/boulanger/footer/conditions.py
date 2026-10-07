from .. import copy, layout
from ..paint import escape_pdf

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    return bool(getattr(doc.visible, "footer_conditions", True) and getattr(doc.visible, "footer", True))

# ----------------------------------------------------------------------

def get_lines(doc) -> list[str]:
    if not is_visible(doc):
        return []

    card = doc.card
    mode = getattr(card, "mode", copy.MODE_EN_LIGNE)
    if mode == copy.MODE_EN_LIGNE:
        return []

    cond_type = getattr(card, "conditions_type", "internet")
    pad = " " * layout.PAD_COLUMNS

    if cond_type == "internet":
        l1 = escape_pdf(f"{pad}Les conditions de vente internet accept\xe9es lors de votre commande sur notre site")
        l2 = escape_pdf(f"{pad}www.boulanger.com, sont les seules applicables \xe0 votre(s) achat(s) \xe0 l'exclusion")
        l3 = escape_pdf(f"{pad}de toutes autres, notamment celles au verso du pr\xe9sent document.")
        return [
            f"() '({l1}) '",
            f"({l2}) '",
            f"({l3}) '",
        ]
    elif cond_type == "pro":
        u_pro = getattr(card, "usage_pro", "NON")
        livr = getattr(card, "livraison", "NON")
        mes = getattr(card, "mise_en_service", "NON")
        c1 = escape_pdf(f"{pad}CLIENT PROFESSIONNEL   : {u_pro}")
        c2 = escape_pdf(f"{pad}LIVRAISON              : {livr}")
        c3 = escape_pdf(f"{pad}MISE EN SERVICE        : {mes}")
        return [
            f"() '({c1}) '",
            f"({c2}) '",
            f"({c3}) '",
        ]

    return []

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
