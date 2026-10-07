"""Footer = filet, mentions, pagination (kind fixé à la création de la page)."""

from .. import flow

from . import legal, line, page


def draw(c, doc, plan):
    if not doc.visible.footer:
        return
    rule_y, legal_ys, page_y, lines = flow.footer_spec(plan.footer_kind)
    line.draw(c, doc, rule_y)
    legal.draw(c, doc, legal_ys, lines)
    page.draw(c, doc, page_y, plan.index + 1, plan.count)
