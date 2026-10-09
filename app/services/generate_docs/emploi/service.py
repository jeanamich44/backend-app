import base64
import io
import zipfile
import pymupdf as fitz

from app.services.generate_docs.emploi.fiche_de_paie.data import from_payload
from app.services.generate_docs.emploi.fiche_de_paie.generate import generate
from app.services.generate_docs.emploi.fiche_de_paie.preview import pack_pdf_bytes
from app.services.generate_docs.emploi.fiche_de_paie.services.orchestration import generate_payroll_sequence
from app.services.generate_docs.common.date_validation import validate_calendar_date
from app.services.generate_docs.common.preview import add_preview_watermark

# ----------------------------------------------------------------------

ISSUERS = ("fiche_de_paie",)

FRENCH_MONTHS = [
    "Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"
]

# ----------------------------------------------------------------------


def validate_fiche_de_paie_payload(payload: dict | None) -> None:
    if not payload:
        return
    for k, v in payload.items():
        if not v or not isinstance(v, str):
            continue
        k_lower = k.lower()
        if "date" in k_lower and not k_lower.startswith(("has_", "show_")):
            if v.lower() not in ("true", "false", "none"):
                label = k.replace("_", " ").capitalize()
                validate_calendar_date(v, label)


def generate_fiche_de_paie_preview_pdf_bytes(payload: dict | None = None) -> bytes:
    p = payload or {}
    validate_fiche_de_paie_payload(p)
    try:
        dur = int(p.get("duree_mois", 1))
    except (ValueError, TypeError):
        dur = 1
    dur = max(1, min(24, dur))
    return pack_pdf_bytes(p, count=dur)


def generate_fiche_de_paie_preview_pages(payload: dict | None = None) -> list[str]:
    pdf_raw = generate_fiche_de_paie_preview_pdf_bytes(payload)
    watermarked = add_preview_watermark(pdf_raw)
    doc = fitz.open(stream=watermarked, filetype="pdf")
    pages_b64 = []
    for page in doc:
        pix = page.get_pixmap(dpi=150, alpha=False)
        jpg_bytes = pix.tobytes(output="jpeg", jpg_quality=75)
        pages_b64.append(base64.b64encode(jpg_bytes).decode("ascii"))
    doc.close()
    return pages_b64


def generate_fiche_de_paie_bytes(payload: dict | None = None) -> tuple[bytes, str, str]:
    p = payload or {}
    validate_fiche_de_paie_payload(p)
    try:
        dur = int(p.get("duree_mois", 1))
    except (ValueError, TypeError):
        dur = 1
    dur = max(1, min(24, dur))

    if dur == 1:
        docs = generate_payroll_sequence(p, count=1)
        doc = docs[0] if docs else from_payload(p)
        pdf_bytes = pack_pdf_bytes(p, count=1)
        m = 1
        y = 2026
        if doc and hasattr(doc, "periode") and doc.periode.date_debut and "/" in doc.periode.date_debut:
            parts = doc.periode.date_debut.split("/")
            if len(parts) == 3:
                try:
                    m = int(parts[1])
                    y = int(parts[2])
                except (ValueError, TypeError):
                    pass
        month_name = FRENCH_MONTHS[m - 1] if 1 <= m <= 12 else str(m)
        filename = f"Fiche_de_paie_{month_name}_{y}.pdf"
        return pdf_bytes, "application/pdf", filename

    docs = generate_payroll_sequence(p, count=dur)
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for idx, doc in enumerate(docs):
            buf = io.BytesIO()
            generate(doc, dest=buf)
            doc_bytes = buf.getvalue()

            m = idx + 1
            y = 2026
            if hasattr(doc, "periode") and doc.periode.date_debut and "/" in doc.periode.date_debut:
                parts = doc.periode.date_debut.split("/")
                if len(parts) == 3:
                    try:
                        m = int(parts[1])
                        y = int(parts[2])
                    except (ValueError, TypeError):
                        pass
            m_name = FRENCH_MONTHS[m - 1] if 1 <= m <= 12 else str(m)
            doc_filename = f"Fiche_de_paie_{idx + 1:02d}_{m_name}_{y}.pdf"
            zf.writestr(doc_filename, doc_bytes)

    zip_buffer.seek(0)
    zip_bytes = zip_buffer.getvalue()
    zip_filename = f"Fiches_de_paie_{dur}_mois.zip"
    return zip_bytes, "application/zip", zip_filename
