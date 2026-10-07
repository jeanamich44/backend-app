from .. import copy as texts
from .. import layout, rules
from ..chrome import vectors
from ..paint import draw_string, fill, fill_rect, fill_subpaths


def _lines(c, x, ys, lines):
    fill(c, layout.COLOR)
    for y, line in zip(ys, lines):
        draw_string(
            c, x, y, line, layout.FONT, layout.SIZE_BODY,
            max_width=layout.ADDR_MAX_W,
        )


def draw(c, doc):
    if not doc.visible.header_addresses:
        return
    single_line = layout.is_single_line_ship(doc.card)
    magasin = layout.is_magasin(doc.card)
    ship_fill = vectors.SHIP_HEAD_FILL_MAGASIN if single_line else vectors.SHIP_HEAD_FILL
    ship_paths = vectors.SHIP_PATHS_MAGASIN if single_line else vectors.SHIP_PATHS
    mode = (getattr(doc.card, "livraison_mode", "") or "").strip().lower()
    if magasin:
        titles = texts.SHIP_TITLE_MAGASIN
    elif mode == layout.MODE_DOMICILE:
        titles = texts.SHIP_TITLE_DOMICILE
    else:
        titles = texts.SHIP_TITLE
    title_y = layout.SHIP_TITLE_Y_MAGASIN if single_line else layout.SHIP_TITLE_Y
    body_y = layout.SHIP_Y_MAGASIN if single_line else layout.SHIP_Y
    fill_rect(c, *ship_fill, layout.COLOR_GRAY)
    fill_rect(c, *vectors.BILL_HEAD_FILL, layout.COLOR_GRAY)
    fill_subpaths(c, ship_paths + vectors.BILL_PATHS, layout.COLOR_GRAY)
    fill(c, layout.COLOR)
    for y, line in zip(title_y, titles):
        draw_string(
            c, layout.SHIP_TEXT_X, y,
            line, layout.FONT_BOLD, layout.SIZE_BODY,
            max_width=layout.ADDR_MAX_W,
        )
    draw_string(
        c, layout.BILL_TEXT_X, layout.BILL_TITLE_Y,
        texts.BILL_TITLE, layout.FONT_BOLD, layout.SIZE_BODY,
        max_width=layout.ADDR_MAX_W,
    )
    _lines(c, layout.SHIP_TEXT_X, body_y, rules.ship_lines(doc.card))
    _lines(c, layout.BILL_TEXT_X, layout.BILL_Y, rules.bill_lines(doc.card))
