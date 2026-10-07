import datetime
import importlib
import io
import re

from fastapi import HTTPException
from app.services.generate_docs.common import example_dates
from app.services.generate_docs.common.date_validation import validate_calendar_date
from app.services.generate_docs.common.preview import pdf_bytes_to_watermarked_jpg

ISSUERS = ("maxance", "axa")


def validate_assurance_payload(payload: dict) -> None:
    immat = payload.get("immatriculation") or payload.get("vehicule_immat")
    if immat:
        immat_clean = str(immat).strip().upper()
        is_valid = bool(
            re.match(
                r"^([A-Z]{2}-[0-9]{3}-[A-Z]{2}|[0-9]{1,4}-[A-Z]{1,3}-(?:[0-9]{1,3}|2[AB])|[A-Z0-9]{1,4}-[A-Z0-9]{1,4}-[A-Z0-9]{1,4})$",
                immat_clean,
            )
            and 7 <= len(immat_clean) <= 12
        )
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Format d'immatriculation invalide : '{immat_clean}'. Format attendu : AA-120-AA ou 123-ABC-45.",
            )

    for field_key, label in [
        ("date_delivrance", "Date de délivrance / d'édition"),
        ("date_effet", "Date d'effet"),
    ]:
        val = payload.get(field_key)
        if val:
            validate_calendar_date(val, label)



def _normalize(data: dict | None) -> dict:
    payload = dict(data or {})
    if payload.get("date_effet"):
        parts = str(payload["date_effet"]).replace("-", "/").replace(".", "/").split("/")
        if len(parts) == 3:
            payload["date_effet_jour"] = parts[0].zfill(2)
            payload["date_effet_mois"] = parts[1].zfill(2)
            payload["date_effet_annee"] = parts[2]
        raw_effet = str(payload["date_effet"]).strip()
        if " - " not in raw_effet:
            payload["info_effet"] = f"{raw_effet} - 00:00"
        else:
            payload["info_effet"] = raw_effet
    elif not payload.get("info_effet"):
        jour, mois, annee = example_dates.maxance_effet()
        payload["info_effet"] = f"{jour}/{mois}/{annee} - 00:00"

    raw_delivrance = payload.get("date_delivrance") or payload.get("date_edition") or payload.get("edition_date")
    if raw_delivrance:
        raw_deliv = str(raw_delivrance).strip()
        if not raw_deliv.lower().startswith("a "):
            payload["edition_date"] = f"A Rueil-Malmaison, le {raw_deliv}"
        else:
            payload["edition_date"] = raw_deliv
    elif not payload.get("edition_date"):
        payload["edition_date"] = f"A Rueil-Malmaison, le {example_dates.maxance_delivrance()}"

    if not payload.get("date_delivrance"):
        payload["date_delivrance"] = example_dates.maxance_delivrance()
    jour, mois, annee = example_dates.maxance_effet()
    if not payload.get("date_effet_jour"):
        payload["date_effet_jour"] = jour
    if not payload.get("date_effet_mois"):
        payload["date_effet_mois"] = mois
    if not payload.get("date_effet_annee"):
        payload["date_effet_annee"] = annee

    if not payload.get("vehicule") and payload.get("vehicule_marque_modele"):
        payload["vehicule"] = payload["vehicule_marque_modele"]
    if payload.get("vehicule_marque_modele") and not payload.get("vehicule_marque"):
        payload["vehicule_marque"] = payload["vehicule_marque_modele"]
    if payload.get("immatriculation") and not payload.get("vehicule_immat"):
        payload["vehicule_immat"] = payload["immatriculation"]

    if payload.get("nom") and payload.get("prenom"):
        civ = payload.get("civilite", "M.")
        civ_prefix = f"{civ} " if civ else ""
        nom = str(payload["nom"]).strip().upper()
        prenom = str(payload["prenom"]).strip().upper()
        payload["titulaire"] = f"{civ_prefix}{nom} {prenom}".strip()
    if payload.get("cp") or payload.get("ville"):
        cp = str(payload.get("cp") or "").strip()
        ville = str(payload.get("ville") or "").strip().upper()
        if cp or ville:
            payload["cp_ville"] = f"{cp} {ville}".strip()
    if payload.get("titulaire") and not payload.get("destinataire_l1"):
        payload["destinataire_l1"] = payload["titulaire"]
    if payload.get("adresse") and not payload.get("destinataire_l2"):
        payload["destinataire_l2"] = payload["adresse"]
    if payload.get("cp_ville") and not payload.get("destinataire_l3"):
        payload["destinataire_l3"] = payload["cp_ville"]

    if payload.get("num_client") and not payload.get("info_client"):
        payload["info_client"] = payload["num_client"]
    if payload.get("num_contrat") and not payload.get("info_contrat"):
        payload["info_contrat"] = payload["num_contrat"]

    if payload.get("tel_sinistre"):
        tel_s = str(payload["tel_sinistre"]).strip()
        if not tel_s.lower().startswith("par "):
            payload["sinistre_tel_label"] = f"Par Téléphone : {tel_s}"
        else:
            payload["sinistre_tel_label"] = tel_s
    if payload.get("mail_sinistre"):
        payload["sinistre_mail_val"] = str(payload["mail_sinistre"]).strip()
    if payload.get("tel_assistance_france"):
        tel_af = str(payload["tel_assistance_france"]).strip()
        if not tel_af.lower().startswith("depuis "):
            payload["assistance_france"] = f"Depuis la France : {tel_af}"
        else:
            payload["assistance_france"] = tel_af
    if payload.get("tel_assistance_etranger"):
        tel_ae = str(payload["tel_assistance_etranger"]).strip()
        if not tel_ae.lower().startswith("depuis "):
            payload["assistance_etranger"] = f"Depuis l'étranger : {tel_ae}"
        else:
            payload["assistance_etranger"] = tel_ae

    return payload


def generate_pdf_bytes(issuer: str, data: dict | None = None) -> bytes:
    if issuer not in ISSUERS:
        raise ValueError(f"Assureur inconnu: {issuer}")
    payload = _normalize(data)
    validate_assurance_payload(payload)
    data_mod = importlib.import_module(
        f"app.services.generate_docs.assurance.issuers.{issuer}.data"
    )
    gen_mod = importlib.import_module(
        f"app.services.generate_docs.assurance.issuers.{issuer}.generate"
    )
    doc = data_mod.from_payload(payload)
    buf = io.BytesIO()
    gen_mod.generate(doc, dest=buf)
    return buf.getvalue()


def generate_preview_jpg_bytes(issuer: str, data: dict | None = None) -> bytes:
    return pdf_bytes_to_watermarked_jpg(generate_pdf_bytes(issuer, data))
