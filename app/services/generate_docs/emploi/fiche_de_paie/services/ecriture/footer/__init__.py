from . import conges, cumuls, mentions, recapitulatif

# ----------------------------------------------------------------------


def draw(c, doc=None):
    vis = getattr(doc, "visible", None)
    if vis is None or getattr(vis, "footer_conges", True):
        conges.draw(c, doc)
    if vis is None or getattr(vis, "footer_cumuls", True):
        cumuls.draw(c, doc)
    if vis is None or getattr(vis, "footer_recapitulatif", True):
        recapitulatif.draw(c, doc)
    if vis is None or getattr(vis, "footer_mentions", True):
        mentions.draw(c, doc)
