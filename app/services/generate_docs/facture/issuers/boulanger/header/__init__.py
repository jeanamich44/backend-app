from .. import copy
from . import addresses, lateral, title

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    return bool(getattr(doc.visible, "header", True))

# ----------------------------------------------------------------------

def get_lines(doc) -> list[str]:
    if not is_visible(doc):
        return ["() '"] * 9

    mode = getattr(doc.card, "mode", copy.MODE_EN_LIGNE)
    t_line = title.get_line(doc) if title.is_visible(doc) else ""
    a_lines = addresses.get_lines(doc) if addresses.is_visible(doc) else []

    lines = []
    if mode == copy.MODE_MAGASIN:
        lines.append("() '")
        lines.append(f"({t_line}) '" if t_line else "() '")
        if a_lines:
            lines.append(f"() '({a_lines[0]}) '" if a_lines[0] else "() '() '")
            for al in a_lines[1:]:
                if al.startswith("() '"):
                    lines.append(al)
                else:
                    lines.append(f"({al}) '" if al else "() '")
    else:
        lines.append(f"({t_line}) '" if t_line else "() '")
        if a_lines:
            lines.append(f"() '({a_lines[0]}) '" if a_lines[0] else "() '() '")
            for al in a_lines[1:]:
                if al.startswith("() '"):
                    lines.append(al)
                else:
                    lines.append(f"({al}) '" if al else "() '")

    return lines

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
