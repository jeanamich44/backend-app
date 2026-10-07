"""Génération justificatif : un issuer = un moteur ReportLab."""

import importlib
import io

from app.services.generate_docs.common import example_dates
from app.services.generate_docs.common.date_validation import validate_calendar_date, validate_time_format
from app.services.generate_docs.common.preview import pdf_bytes_to_watermarked_jpg
from app.services.generate_docs.justificatif.schemas import parse_justificatif_payload

ISSUERS = ("conduite_heures", "attestation_edf", "attestation_direct_energie")

FILENAMES = {
    "conduite_heures": (
        "Justificatif_Heures_Conduite.pdf",
        "preview_Justificatif_Heures_Conduite.jpg",
        "Heures de conduite",
    ),
    "attestation_edf": (
        "Attestation_EDF.pdf",
        "preview_Attestation_EDF.jpg",
        "Attestation EDF",
    ),
    "attestation_direct_energie": (
        "Attestation_Direct_Energie.pdf",
        "preview_Attestation_Direct_Energie.jpg",
        "Attestation Direct Énergie",
    ),
}


def validate_justificatif_payload(issuer: str, payload: dict | None) -> None:
    if not payload:
        return
    for k, v in payload.items():
        if k == "rdvs" and isinstance(v, list):
            for idx, rdv in enumerate(v, start=1):
                if isinstance(rdv, dict):
                    if rdv.get("date"):
                        validate_calendar_date(rdv["date"], f"Date leçon {idx}")
                    if rdv.get("debut"):
                        validate_time_format(rdv["debut"], f"Heure début leçon {idx}")
                    if rdv.get("fin"):
                        validate_time_format(rdv["fin"], f"Heure fin leçon {idx}")
            continue
        if not v or not isinstance(v, str):
            continue
        k_lower = k.lower()
        if ("date" in k_lower or k_lower in ("edition", "edition_date", "depuis")) and not k_lower.startswith(("has_", "show_")):
            if v.lower() not in ("true", "false", "none"):
                label = k.replace("_", " ").capitalize()
                validate_calendar_date(v, label)
        elif ("time" in k_lower or "heure" in k_lower) and not k_lower.startswith(("has_", "show_")):
            if v.lower() not in ("true", "false", "none"):
                label = k.replace("_", " ").capitalize()
                validate_time_format(v, label)


def generate_pdf_bytes(issuer: str, data: dict | None = None) -> bytes:
    if issuer not in ISSUERS:
        raise ValueError(f"Justificatif inconnu: {issuer}")
    if data:
        validate_justificatif_payload(issuer, data)
    payload = parse_justificatif_payload(issuer, data)
    if issuer == "attestation_edf":
        payload.setdefault("date", example_dates.edf_attestation())
    elif issuer == "conduite_heures":
        payload.setdefault("edition", example_dates.conduite_edition())
        if not payload.get("rdvs"):
            payload["rdvs"] = example_dates.conduite_lessons()
    data_mod = importlib.import_module(
        f"app.services.generate_docs.justificatif.issuers.{issuer}.data"
    )
    gen_mod = importlib.import_module(
        f"app.services.generate_docs.justificatif.issuers.{issuer}.generate"
    )
    doc = data_mod.from_payload(payload)
    buf = io.BytesIO()
    gen_mod.generate(doc, dest=buf)
    return buf.getvalue()


def generate_preview_jpg_bytes(issuer: str, data: dict | None = None) -> bytes:
    return pdf_bytes_to_watermarked_jpg(generate_pdf_bytes(issuer, data))
