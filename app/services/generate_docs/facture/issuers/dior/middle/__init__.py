from . import articles, code, line, page, pay, totals, vendeur

# ----------------------------------------------------------------------

def get_dy(doc) -> float:
    items = getattr(doc.middle, "items", None)
    if items and len(items) > 1:
        return (min(len(items), 3) - 1) * 16.8
    return 0.0

# ----------------------------------------------------------------------

def draw_main(c, doc):
    if not doc.visible.middle:
        return
    if doc.visible.middle_page:
        page.draw(c, doc)
    if doc.visible.middle_vendeur:
        vendeur.draw(c, doc)
    if doc.visible.middle_articles:
        articles.draw(c, doc)

    dy = get_dy(doc)
    if dy:
        c.saveState()
        c.translate(0, -dy)

    if doc.visible.middle_line:
        line.draw(c, doc)
    if doc.visible.middle_totals:
        totals.draw(c, doc)

    if dy:
        c.restoreState()

# ----------------------------------------------------------------------

def draw_bottom(c, doc):
    if not doc.visible.middle:
        return

    dy = get_dy(doc)
    if dy:
        c.saveState()
        c.translate(0, -dy)

    if doc.visible.middle_pay:
        pay.draw(c, doc)
    if doc.visible.middle_code:
        code.draw(c, doc)

    if dy:
        c.restoreState()

# ----------------------------------------------------------------------

def draw(c, doc):
    draw_main(c, doc)
    draw_bottom(c, doc)
