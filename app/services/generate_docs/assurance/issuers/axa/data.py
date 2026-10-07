from dataclasses import dataclass, field

from . import copy as texts

# ----------------------------------------------------------------------


@dataclass
class HeaderData:
    destinataire_l1: str = texts.DESTINATAIRE_L1
    destinataire_l2: str = texts.DESTINATAIRE_L2
    destinataire_l3: str = texts.DESTINATAIRE_L3
    edition_date: str = field(default_factory=texts.default_edition_date)
    rappel_title: str = texts.RAPPEL_TITLE
    rappel_l1: str = texts.RAPPEL_L1
    rappel_l2: str = texts.RAPPEL_L2
    rappel_l3: str = texts.RAPPEL_L3
    memo_title: str = texts.MEMO_TITLE
    memo_conserver: str = texts.MEMO_CONSERVER
    notice_l1: str = texts.NOTICE_L1
    notice_l2: str = texts.NOTICE_L2
    presomption_souligne: str = texts.PRESOMPTION_SOULIGNE
    presomption_valable: str = texts.PRESOMPTION_VALABLE
    obligation_fva_l1: str = texts.OBLIGATION_FVA_L1
    obligation_fva_l2: str = texts.OBLIGATION_FVA_L2
    politesse: str = texts.POLITESSE


@dataclass
class MiddleData:
    vehicule_title: str = texts.VEHICULE_TITLE
    info_title: str = texts.INFO_TITLE
    info_client: str = texts.INFO_CLIENT
    info_contrat: str = texts.INFO_CONTRAT
    info_effet: str = field(default_factory=texts.default_info_effet)
    vehicule_subtitle: str = texts.VEHICULE_SUBTITLE
    vehicule_marque: str = texts.VEHICULE_MARQUE
    vehicule_immat: str = texts.VEHICULE_IMMAT
    remorque_title: str = texts.REMORQUE_TITLE
    remorque_l1: str = texts.REMORQUE_L1
    remorque_l2: str = texts.REMORQUE_L2
    assureur_title: str = texts.ASSUREUR_TITLE
    assureur_nom: str = texts.ASSUREUR_NOM
    assureur_adresse: str = texts.ASSUREUR_ADRESSE
    couverture_l1: str = texts.COUVERTURE_L1
    couverture_l2: str = texts.COUVERTURE_L2


@dataclass
class FooterData:
    numeros_title: str = texts.NUMEROS_TITLE
    numeros_subtitle: str = texts.NUMEROS_SUBTITLE
    sinistre_header: str = texts.SINISTRE_HEADER
    sinistre_intro: str = texts.SINISTRE_INTRO
    sinistre_service: str = texts.SINISTRE_SERVICE
    sinistre_mail_label: str = texts.SINISTRE_MAIL_LABEL
    sinistre_mail_val: str = texts.SINISTRE_MAIL_VAL
    sinistre_tel_label: str = texts.SINISTRE_TEL_LABEL
    sinistre_horaires: str = texts.SINISTRE_HORAIRES
    assistance_header: str = texts.ASSISTANCE_HEADER
    assistance_intro: str = texts.ASSISTANCE_INTRO
    assistance_service: str = texts.ASSISTANCE_SERVICE
    assistance_france: str = texts.ASSISTANCE_FRANCE
    assistance_etranger: str = texts.ASSISTANCE_ETRANGER
    questions_text: str = texts.QUESTIONS_TEXT
    renvoi_l1: str = texts.RENVOI_L1
    renvoi_l2: str = texts.RENVOI_L2
    legal_l1: str = texts.LEGAL_L1
    legal_l2: str = texts.LEGAL_L2
    legal_l3: str = texts.LEGAL_L3
    legal_l4: str = texts.LEGAL_L4


@dataclass
class VisibleData:
    header: bool = True
    header_logo: bool = True
    header_recipient: bool = True
    header_carte_verte: bool = True
    header_notice: bool = True
    header_presomption: bool = True
    middle: bool = True
    middle_vehicule: bool = True
    middle_remorque: bool = True
    middle_assureur: bool = True
    middle_couverture: bool = True
    footer: bool = True
    footer_numeros_utiles: bool = True
    footer_questions: bool = True
    footer_legal: bool = True


@dataclass
class Doc:
    header: HeaderData = field(default_factory=HeaderData)
    middle: MiddleData = field(default_factory=MiddleData)
    footer: FooterData = field(default_factory=FooterData)
    visible: VisibleData = field(default_factory=VisibleData)


def from_payload(payload: dict | None = None) -> Doc:
    p = dict(payload or {})
    doc = Doc()
    for k, v in p.items():
        if hasattr(doc.header, k):
            setattr(doc.header, k, v)
        elif hasattr(doc.middle, k):
            setattr(doc.middle, k, v)
        elif hasattr(doc.footer, k):
            setattr(doc.footer, k, v)
        elif hasattr(doc.visible, k):
            setattr(doc.visible, k, bool(v))
    if isinstance(p.get("visible"), dict):
        for k, v in p["visible"].items():
            if hasattr(doc.visible, k):
                setattr(doc.visible, k, bool(v))
    return doc
