import importlib
import io

from app.services.generate_docs.common.date_validation import validate_calendar_date, validate_time_format
from app.services.generate_docs.common.preview import pdf_bytes_to_watermarked_jpg
from app.services.generate_docs.rib.payload import to_lab_payload

BANKS = (
    "lbp", "ca", "sg", "cm", "cic", "qonto", "helios", "lcl", "bp",
    "bnp", "bfb", "ce", "boursobank", "revolut", "noelse", "sumup", "mypos",
)

FILENAMES = {
    "lbp": ("RIB_LBP.pdf", "preview_RIB_LBP.jpg", "LBP"),
    "ca": ("RIB_CA.pdf", "preview_RIB_CA.jpg", "CA"),
    "sg": ("RIB_SG.pdf", "preview_RIB_SG.jpg", "SG"),
    "cm": ("RIB_CM.pdf", "preview_RIB_CM.jpg", "CM"),
    "cic": ("RIB_CIC.pdf", "preview_RIB_CIC.jpg", "CIC"),
    "qonto": ("RIB_QONTO.pdf", "preview_RIB_QONTO.jpg", "Qonto"),
    "helios": ("RIB_HELIOS.pdf", "preview_RIB_HELIOS.jpg", "Helios"),
    "lcl": ("RIB_LCL.pdf", "preview_RIB_LCL.jpg", "LCL"),
    "bp": ("RIB_BP.pdf", "preview_RIB_BP.jpg", "BP"),
    "bnp": ("RIB_BNP.pdf", "preview_RIB_BNP.jpg", "BNP"),
    "bfb": ("RIB_BFB.pdf", "preview_RIB_BFB.jpg", "BFB"),
    "ce": ("RIB_CE.pdf", "preview_RIB_CE.jpg", "CE"),
    "boursobank": ("RIB_BoursoBank.pdf", "preview_RIB_BoursoBank.jpg", "BoursoBank"),
    "revolut": ("RIB_REVOLUT.pdf", "preview_RIB_REVOLUT.jpg", "Revolut"),
    "noelse": ("RIB_NOELSE.pdf", "preview_RIB_NOELSE.jpg", "Noelse"),
    "sumup": ("Account_Details_SumUp.pdf", "preview_Account_Details_SumUp.jpg", "SumUp"),
    "mypos": ("Certificat_IBAN_myPOS.pdf", "preview_Certificat_IBAN_myPOS.jpg", "MyPOS"),
}


def validate_rib_payload(bank: str, payload: dict | None) -> None:
    if not payload:
        return
    for k, v in payload.items():
        if not v or not isinstance(v, str):
            continue
        k_lower = k.lower()
        if ("date" in k_lower or k_lower == "middle_date") and not k_lower.startswith(("has_", "show_")):
            if v.lower() not in ("true", "false", "none"):
                label = k.replace("_", " ").capitalize()
                validate_calendar_date(v, label)
        elif ("time" in k_lower or "heure" in k_lower) and not k_lower.startswith(("has_", "show_")):
            if v.lower() not in ("true", "false", "none"):
                label = k.replace("_", " ").capitalize()
                validate_time_format(v, label)


def generate_pdf_bytes(bank: str, data: dict | None = None) -> bytes:
    if data:
        validate_rib_payload(bank, data)
    payload = to_lab_payload(bank, data)
    data_mod = importlib.import_module(f"app.services.generate_docs.rib.banks.{bank}.data")
    gen_mod = importlib.import_module(f"app.services.generate_docs.rib.banks.{bank}.generate")
    doc = data_mod.from_payload(payload)
    buf = io.BytesIO()
    gen_mod.generate(doc, dest=buf)
    return buf.getvalue()


def generate_preview_jpg_bytes(bank: str, data: dict | None = None) -> bytes:
    return pdf_bytes_to_watermarked_jpg(generate_pdf_bytes(bank, data))
