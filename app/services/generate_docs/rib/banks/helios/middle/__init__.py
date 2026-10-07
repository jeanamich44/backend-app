"""Middle : notice, titulaire, IBAN/BIC, tableau RIB, notes, cadres."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill
from . import bic, domiciliation, iban, lines, notice, notes, table, titulaire


def _intl_title(c, doc, dy=0):
    vis = doc.visible
    if not (vis.middle_iban or vis.middle_bic or vis.middle_domiciliation):
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.INTL_TITLE_X, layout.INTL_TITLE_Y + dy, texts.INTL_TITLE,
        layout.FONT_BOLD, layout.SIZE_SECTION,
    )


def draw(c, doc):
    if not doc.visible.middle:
        return
    lines.draw(c, doc)
    notice.draw(c, doc)
    titulaire.draw(c, doc)
    _intl_title(c, doc)
    iban.draw(c, doc)
    bic.draw(c, doc)
    domiciliation.draw(c, doc)
    table.draw(c, doc)
    notes.draw(c, doc)
