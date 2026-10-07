from . import articles, club, notice, payment, table_header, totals

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    return bool(getattr(doc.visible, "middle", True))

# ----------------------------------------------------------------------

def get_lines(doc) -> list[str]:
    if not is_visible(doc):
        return []

    lines = []
    if table_header.is_visible(doc):
        lines.append(table_header.get_line(doc))
    if articles.is_visible(doc):
        lines.extend(articles.get_lines(doc))
    if club.is_visible(doc):
        lines.extend(club.get_lines(doc))
    if totals.is_visible(doc):
        lines.extend(totals.get_lines(doc))
    if payment.is_visible(doc):
        lines.extend(payment.get_lines(doc))
    if notice.is_visible(doc):
        lines.extend(notice.get_lines(doc))

    return lines

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
