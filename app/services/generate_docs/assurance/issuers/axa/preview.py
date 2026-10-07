import tempfile
from pathlib import Path

import fitz

from . import copy as texts
from . import rules
from .data import from_payload
from .generate import generate

# ----------------------------------------------------------------------


def defaults() -> dict:
    return {
        "destinataire_l1": texts.DESTINATAIRE_L1,
        "destinataire_l2": texts.DESTINATAIRE_L2,
        "destinataire_l3": texts.DESTINATAIRE_L3,
        "edition_date": texts.default_edition_date(),
        "rappel_title": texts.RAPPEL_TITLE,
        "rappel_l1": texts.RAPPEL_L1,
        "rappel_l2": texts.RAPPEL_L2,
        "rappel_l3": texts.RAPPEL_L3,
        "memo_title": texts.MEMO_TITLE,
        "memo_conserver": texts.MEMO_CONSERVER,
        "notice_l1": texts.NOTICE_L1,
        "notice_l2": texts.NOTICE_L2,
        "presomption_souligne": texts.PRESOMPTION_SOULIGNE,
        "presomption_valable": texts.PRESOMPTION_VALABLE,
        "obligation_fva_l1": texts.OBLIGATION_FVA_L1,
        "obligation_fva_l2": texts.OBLIGATION_FVA_L2,
        "politesse": texts.POLITESSE,
        "vehicule_title": texts.VEHICULE_TITLE,
        "info_title": texts.INFO_TITLE,
        "info_client": texts.INFO_CLIENT,
        "info_contrat": texts.INFO_CONTRAT,
        "info_effet": texts.default_info_effet(),
        "vehicule_subtitle": texts.VEHICULE_SUBTITLE,
        "vehicule_marque": texts.VEHICULE_MARQUE,
        "vehicule_immat": texts.VEHICULE_IMMAT,
        "remorque_title": texts.REMORQUE_TITLE,
        "remorque_l1": texts.REMORQUE_L1,
        "remorque_l2": texts.REMORQUE_L2,
        "assureur_title": texts.ASSUREUR_TITLE,
        "assureur_nom": texts.ASSUREUR_NOM,
        "assureur_adresse": texts.ASSUREUR_ADRESSE,
        "couverture_l1": texts.COUVERTURE_L1,
        "couverture_l2": texts.COUVERTURE_L2,
        "numeros_title": texts.NUMEROS_TITLE,
        "numeros_subtitle": texts.NUMEROS_SUBTITLE,
        "sinistre_header": texts.SINISTRE_HEADER,
        "sinistre_intro": texts.SINISTRE_INTRO,
        "sinistre_service": texts.SINISTRE_SERVICE,
        "sinistre_mail_label": texts.SINISTRE_MAIL_LABEL,
        "sinistre_mail_val": texts.SINISTRE_MAIL_VAL,
        "sinistre_tel_label": texts.SINISTRE_TEL_LABEL,
        "sinistre_horaires": texts.SINISTRE_HORAIRES,
        "assistance_header": texts.ASSISTANCE_HEADER,
        "assistance_intro": texts.ASSISTANCE_INTRO,
        "assistance_service": texts.ASSISTANCE_SERVICE,
        "assistance_france": texts.ASSISTANCE_FRANCE,
        "assistance_etranger": texts.ASSISTANCE_ETRANGER,
        "questions_text": texts.QUESTIONS_TEXT,
        "renvoi_l1": texts.RENVOI_L1,
        "renvoi_l2": texts.RENVOI_L2,
        "legal_l1": texts.LEGAL_L1,
        "legal_l2": texts.LEGAL_L2,
        "legal_l3": texts.LEGAL_L3,
        "legal_l4": texts.LEGAL_L4,
        "_limits": rules.public_limits(),
        "_rules": rules.public_rules(),
    }


def pdf_bytes(payload: dict | None = None) -> bytes:
    doc = from_payload(payload)
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        path = Path(tmp.name)
    try:
        generate(doc, dest=path)
        return path.read_bytes()
    finally:
        path.unlink(missing_ok=True)


def png_from_pdf(pdf: bytes, scale: float = 2.0) -> bytes:
    doc = fitz.open(stream=pdf, filetype="pdf")
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    doc.close()
    return pix.tobytes("png")


def png_bytes(payload: dict | None = None, scale: float = 2.0) -> bytes:
    return png_from_pdf(pdf_bytes(payload), scale)
