import io
from reportlab.pdfgen import canvas
from app.services.generate_docs.common.fonts import register
from . import footer, header, layout, middle, static
from .data import FactureChannel

# ----------------------------------------------------------------------

def _fonts():
    register(layout.FONT_REGULAR, layout.FONT_REGULAR_FILE)
    register(layout.FONT_BOLD, layout.FONT_BOLD_FILE)

# ----------------------------------------------------------------------

def generate(doc: FactureChannel | None = None, dest=None):
    doc = doc or FactureChannel()
    _fonts()
    buf = dest if dest is not None else io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(layout.PAGE_W, layout.PAGE_H))

    static.draw(c, doc)
    header.draw(c, doc)
    middle.draw(c, doc)
    footer.draw(c, doc)

    c.showPage()
    c.save()
    if dest is None:
        return buf.getvalue()
    return dest

# ----------------------------------------------------------------------

generate_pdf = generate
