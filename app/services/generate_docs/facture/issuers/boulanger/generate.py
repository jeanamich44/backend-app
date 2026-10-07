import io
import tempfile
from pathlib import Path
import fitz
from . import copy, footer, header, middle, paint, rules
from .data import Doc, FactureBoulanger, from_payload

# ----------------------------------------------------------------------

def generate(doc: FactureBoulanger | dict | None = None, dest=None):
    if isinstance(doc, dict):
        doc = from_payload(doc)
    else:
        doc = rules.apply_doc(doc or Doc())

    template_bytes = paint.get_template_bytes()
    doc_pdf = fitz.open(stream=template_bytes, filetype="pdf")
    xi0_xref, xi1_xref, text_xref, invoke_xref = paint.get_template_xrefs(doc_pdf)

    mode = getattr(doc.card, "mode", copy.MODE_EN_LIGNE)

    t_lines = [
        "BT\r",
        "/F1 8.3 Tf 0 842 Td 12.7 TL\r",
    ]

    h_lines = header.get_lines(doc)
    for hl in h_lines:
        t_lines.append(f"{hl}\r")

    if mode == copy.MODE_MAGASIN:
        t_lines.extend([
            "() '\r",
            "()() '\r",
            "() '\r",
            "()() '\r",
            "() '\r",
            "()() '\r",
        ])
    else:
        t_lines.extend([
            "() '\r",
            "()() '\r",
            "() '\r",
        ])

    m_lines = middle.get_lines(doc)
    for ml in m_lines:
        t_lines.append(f"{ml}\r")

    c_lines = footer.conditions.get_lines(doc) if footer.conditions.is_visible(doc) else []
    for cl in c_lines:
        t_lines.append(f"{cl}\r")

    target_company_idx = 40 if mode == copy.MODE_MAGASIN else 39
    current_idx = len(t_lines)
    pad_needed = max(1, target_company_idx - current_idx)

    for i in range(pad_needed):
        empty_token = "()() '\r" if (i % 2 == 1) else "() '\r"
        t_lines.append(empty_token)

    if footer.company.is_visible(doc):
        comp_lines = footer.company.get_lines(doc)
        for cl in comp_lines:
            t_lines.append(f"{cl}\r")

    t_lines.append("ET\r")

    text_stream = "\n".join(t_lines).encode("latin1")
    doc_pdf.update_stream(text_xref, text_stream)

    show_logo = header.lateral.logo.is_visible(doc)
    show_sidebar = header.lateral.sidebar.is_visible(doc)
    show_legal = footer.legal.is_visible(doc)
    show_barcode = header.lateral.barcode.is_visible(doc)

    show_xi0 = show_logo or show_sidebar or show_legal
    show_xi1 = show_barcode

    x_lines = [" Q\r", "q\r"]
    if show_xi0:
        x_lines.append("q 1 0 0 1 0 0 cm /Xi0 Do Q\r")
    if show_xi1:
        x_lines.append("q 1 0 0 1 32 592 cm /Xi1 Do Q\r")
    x_lines.append("Q\r")
    s40 = "\n".join(x_lines).encode("latin1")
    doc_pdf.update_stream(invoke_xref, s40)

    logo_str, sidebar_str, legal_str = paint.get_xi0_parts(doc_pdf, xi0_xref)
    xi0_active = []
    if show_logo:
        xi0_active.append(logo_str)
    if show_sidebar:
        xi0_active.append(sidebar_str)
    if show_legal:
        xi0_active.append(legal_str)
    xi0_stream = "\n".join(xi0_active).encode("latin1")
    doc_pdf.update_stream(xi0_xref, xi0_stream)

    if show_barcode:
        barcode_stream = header.lateral.barcode.get_stream(doc)
        doc_pdf.update_stream(xi1_xref, barcode_stream)

    buf = doc_pdf.tobytes(deflate=True, clean=True)
    doc_pdf.close()

    if dest is None:
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        tmp.write(buf)
        tmp.close()
        return Path(tmp.name)
    if isinstance(dest, io.BytesIO):
        dest.write(buf)
        dest.seek(0)
        return dest
    if isinstance(dest, (str, Path)):
        Path(dest).write_bytes(buf)
    return dest

# ----------------------------------------------------------------------

generate_pdf = generate
