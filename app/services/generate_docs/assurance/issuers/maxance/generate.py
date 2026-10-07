"""Assemble header, middle, footer."""

from reportlab.pdfbase import pdfdoc, pdfmetrics
from reportlab.pdfbase.pdfmetrics import Font

from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import register, set_pdf_metrics

from . import chrome, footer, header, layout, middle, rules, static
from .data import Doc


class _ArialObliqueType1(Font):
    """Type1 /Arial-Oblique non embarqué, comme le gabarit (0 Tr, substitution visor)."""

    def addObjects(self, doc):
        internal_name = "F" + repr(len(doc.fontMapping) + 1)
        pdf_font = pdfdoc.PDFType1Font()
        pdf_font.Name = internal_name
        pdf_font.BaseFont = "Arial-Oblique"
        pdf_font.Encoding = pdfdoc.PDFName("WinAnsiEncoding")
        pdf_font.FirstChar = 32
        pdf_font.LastChar = 255
        pdf_font.Widths = pdfdoc.PDFArray(self.widths[32:256])
        descriptor = pdfdoc.PDFDictionary({
            "Type": "/FontDescriptor",
            "Ascent": 895,
            "Descent": -210,
            "FontBBox": pdfdoc.PDFArray([-517, -325, 1359, 998]),
            "MissingWidth": 750,
            "CapHeight": 716,
            "FontName": pdfdoc.PDFName("Arial-Oblique"),
            "ItalicAngle": -12,
            "Flags": 96,
            "StemV": 100,
        })
        pdf_font.FontDescriptor = doc.Reference(descriptor, "FD:Arial-Oblique")
        doc.Reference(pdf_font, internal_name)
        doc.idToObject["BasicFonts"].dict[internal_name] = pdf_font
        doc.fontMapping[self.fontName] = "/" + internal_name


def _register_arial_oblique():
    if "Arial-Oblique" in pdfmetrics._fonts:
        return
    pdfmetrics.getFont("Helvetica-Oblique")
    pdfmetrics.registerFont(
        _ArialObliqueType1("Arial-Oblique", "Helvetica-Oblique", "WinAnsiEncoding")
    )


def _fonts():
    register(layout.FONT, layout.FONT_FILE)
    register(layout.FONT_BOLD, layout.FONT_BOLD_FILE)
    _register_arial_oblique()
    set_pdf_metrics(
        layout.FONT, layout.FONT_ASCENT, layout.FONT_DESCENT,
        layout.FONT_BBOX, layout.FONT_CAP,
    )
    set_pdf_metrics(
        layout.FONT_BOLD, layout.FONT_BOLD_ASCENT, layout.FONT_BOLD_DESCENT,
        layout.FONT_BOLD_BBOX, layout.FONT_CAP,
    )


def generate(doc=None, dest=None):
    doc = rules.apply_doc(doc or Doc())
    _fonts()
    pagesize = (layout.PAGE_W, layout.PAGE_H)
    c, out = new_pdf(pagesize=pagesize, dest=dest)
    chrome.draw(c, doc)
    header.draw(c, doc)
    middle.draw(c, doc)
    footer.draw(c, doc)
    static.draw(c, doc)
    c.showPage()
    c.save()
    return out


if __name__ == "__main__":
    print(generate())
