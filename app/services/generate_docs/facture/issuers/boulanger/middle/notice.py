from .. import copy
from ..paint import escape_pdf

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    return bool(getattr(doc.visible, "middle_notice", True) and getattr(doc.visible, "middle", True))

# ----------------------------------------------------------------------

def get_lines(doc) -> list[str]:
    if not is_visible(doc):
        return []

    card = doc.card
    mode = getattr(card, "mode", copy.MODE_EN_LIGNE)

    lines_text = []
    if mode == copy.MODE_EN_LIGNE:
        cumul_text = getattr(card, "notice_cumul", copy.EL_NOTICE_CUMUL)
        if cumul_text:
            lines_text.append(f"{' ' * 51}{cumul_text}")

    merci_text = getattr(card, "notice_merci", copy.NOTICE_MERCI)
    if merci_text:
        lines_text.append(f"{' ' * 66}{merci_text}")

    g1 = getattr(card, "notice_garantie_1", copy.NOTICE_GARANTIE_L1)
    g2 = getattr(card, "notice_garantie_2", copy.NOTICE_GARANTIE_L2)
    g3 = getattr(card, "notice_garantie_3", copy.NOTICE_GARANTIE_L3)

    if g1:
        lines_text.append(f"{' ' * 58}{g1}")
    if g2:
        lines_text.append(f"{' ' * 58}{g2}")
    if g3:
        lines_text.append(f"{' ' * 73}{g3}")

    if not lines_text:
        return []

    result = ["() '"]
    first = True
    for lt in lines_text:
        esc = escape_pdf(lt)
        if first:
            result.append(f"()({esc}) '")
            first = False
        else:
            result.append(f"({esc}) '")

    return result

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
