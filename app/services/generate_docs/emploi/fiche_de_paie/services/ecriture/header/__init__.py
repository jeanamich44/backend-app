from . import convention, employeur, periode, salarie, titre

# ----------------------------------------------------------------------


def draw(c, doc=None):
    vis = getattr(doc, "visible", None)
    if vis is None or getattr(vis, "header_employeur", True):
        employeur.draw(c, doc)
    if vis is None or getattr(vis, "header_titre", True):
        titre.draw(c, doc)
    if vis is None or getattr(vis, "header_periode", True):
        periode.draw(c, doc)
    if vis is None or getattr(vis, "header_salarie", True):
        salarie.draw(c, doc)
    if vis is None or getattr(vis, "header_convention", True):
        convention.draw(c, doc)
