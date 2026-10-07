import io
from reportlab.pdfgen import canvas
from app.services.generate_docs.common.fonts import register, set_pdf_metrics
from . import header, layout, middle, static
from .data import FactureNocibe, from_payload

# ----------------------------------------------------------------------

def _fonts():
    register(layout.FONT_REGULAR, layout.FONT_REGULAR_FILE)
    register(layout.FONT_BOLD, layout.FONT_BOLD_FILE)
    register(layout.FONT_ITALIC, layout.FONT_ITALIC_FILE)
    register(layout.FONT_SANS, layout.FONT_SANS_FILE)
    set_pdf_metrics(
        layout.FONT_REGULAR,
        layout.FONT_REGULAR_ASCENT,
        layout.FONT_REGULAR_DESCENT,
        layout.FONT_REGULAR_BBOX,
        layout.FONT_REGULAR_CAP,
        flags=layout.FONT_REGULAR_FLAGS,
        stem_v=layout.FONT_REGULAR_STEMV,
    )
    set_pdf_metrics(
        layout.FONT_BOLD,
        layout.FONT_BOLD_ASCENT,
        layout.FONT_BOLD_DESCENT,
        layout.FONT_BOLD_BBOX,
        layout.FONT_BOLD_CAP,
        flags=layout.FONT_BOLD_FLAGS,
        stem_v=layout.FONT_BOLD_STEMV,
    )
    set_pdf_metrics(
        layout.FONT_ITALIC,
        layout.FONT_ITALIC_ASCENT,
        layout.FONT_ITALIC_DESCENT,
        layout.FONT_ITALIC_BBOX,
        layout.FONT_ITALIC_CAP,
        flags=layout.FONT_ITALIC_FLAGS,
        stem_v=layout.FONT_ITALIC_STEMV,
    )
    set_pdf_metrics(
        layout.FONT_SANS,
        layout.FONT_SANS_ASCENT,
        layout.FONT_SANS_DESCENT,
        layout.FONT_SANS_BBOX,
        layout.FONT_SANS_CAP,
        flags=layout.FONT_SANS_FLAGS,
        stem_v=layout.FONT_SANS_STEMV,
    )

# ----------------------------------------------------------------------

def generate(doc: FactureNocibe | dict | None = None, dest=None):
    if isinstance(doc, dict):
        doc = from_payload(doc)
    else:
        doc = doc or FactureNocibe()
    _fonts()
    buf = dest if dest is not None else io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(layout.PAGE_W, layout.PAGE_H))

    static.draw(c, doc)
    header.draw(c, doc)
    middle.draw(c, doc)

    c.showPage()
    c.save()
    if dest is None:
        return buf.getvalue()
    return dest

# ----------------------------------------------------------------------

generate_pdf = generate
