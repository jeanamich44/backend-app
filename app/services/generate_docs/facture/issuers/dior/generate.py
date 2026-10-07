import io
from reportlab.pdfgen import canvas
from . import footer, header, layout, middle, static
from .data import FactureDior
from .font_dior import attach_dior_fonts

# ----------------------------------------------------------------------

def generate(doc: FactureDior | None = None, dest=None):
    doc = doc or FactureDior()
    buf = dest if dest is not None else io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(layout.PAGE_W, layout.PAGE_H))
    attach_dior_fonts(c)

    header.draw(c, doc)
    middle.draw_main(c, doc)
    header.draw_bg(c, doc)
    middle.draw_bottom(c, doc)
    footer.draw(c, doc)
    static.draw(c, doc)

    c.showPage()
    c.save()
    if dest is None:
        return buf.getvalue()
    return dest

# ----------------------------------------------------------------------

generate_pdf = generate
