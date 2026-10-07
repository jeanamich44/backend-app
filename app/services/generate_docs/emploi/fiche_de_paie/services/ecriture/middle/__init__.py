from . import impot_source, net_avant_impot, tableau_cotisations

# ----------------------------------------------------------------------


def draw(c, doc=None):
    vis = getattr(doc, "visible", None)
    if vis is None or getattr(vis, "middle_tableau_cotisations", True):
        tableau_cotisations.draw(c, doc)
    if vis is None or getattr(vis, "middle_net_avant_impot", True):
        net_avant_impot.draw(c, doc)
    if vis is None or getattr(vis, "middle_impot_source", True):
        impot_source.draw(c, doc)
