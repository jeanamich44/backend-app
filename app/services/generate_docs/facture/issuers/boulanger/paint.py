from pathlib import Path
from . import layout

# ----------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PDF_PATH = BASE_DIR / "template.pdf"

_cached_template = None
_cached_xi0_parts = None

# ----------------------------------------------------------------------

def get_template_bytes() -> bytes:
    global _cached_template
    if _cached_template is None:
        _cached_template = TEMPLATE_PDF_PATH.read_bytes()
    return _cached_template

# ----------------------------------------------------------------------

def get_template_xrefs(doc_pdf) -> tuple[int, int, int, int]:
    page = doc_pdf[0]
    xi0_xref, xi1_xref = 16, 17
    for xref, name, _, _ in page.get_xobjects():
        if name == "Xi0":
            xi0_xref = xref
        elif name == "Xi1":
            xi1_xref = xref
    text_xref, invoke_xref = 11, 12
    for c in page.get_contents():
        s = doc_pdf.xref_stream(c)
        if b"BT" in s:
            text_xref = c
        elif b"Do" in s:
            invoke_xref = c
    return xi0_xref, xi1_xref, text_xref, invoke_xref

# ----------------------------------------------------------------------

def get_xi0_parts(doc_orig, xi0_xref: int = 16) -> tuple[str, str, str]:
    global _cached_xi0_parts
    if _cached_xi0_parts is None:
        s = doc_orig.xref_stream(xi0_xref).decode("latin1")
        lines = s.splitlines()
        logo = "\n".join(lines[:374])
        sidebar = "\n".join(lines[374:1888])
        legal = "\n".join(lines[1888:])
        _cached_xi0_parts = (logo, sidebar, legal)
    return _cached_xi0_parts

# ----------------------------------------------------------------------

def escape_pdf(text: str) -> str:
    return str(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

# ----------------------------------------------------------------------

def get_barcode_stream(value: str | None = None) -> bytes:
    bars = layout.get_barcode_bars(value)
    lines = []
    for bx, bw in bars:
        lines.append(f"{bx:g} 9.6 {bw:g} 32 re")
    lines.append("f")
    lines.append("BT")
    lines.append("/F1 8 Tf")
    lines.append("1 0 0 1 67.2 1.6 Tm")
    lines.append("()Tj")
    lines.append("ET\r")
    return "\r\n".join(lines).encode("latin1")
