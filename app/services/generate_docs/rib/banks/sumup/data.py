"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import rules


@dataclass
class Header:
    title: str = texts.TITLE
    date: str = field(default_factory=lambda: texts.DATE)


@dataclass
class Card:
    titulaire_nom: str = texts.TITULAIRE_NOM
    titulaire_adresse: str = texts.TITULAIRE_ADRESSE
    titulaire_ville: str = texts.TITULAIRE_VILLE
    titulaire_pays: str = texts.TITULAIRE_PAYS
    date_ouverture: str = field(default_factory=lambda: texts.DATE_OUVERTURE)
    institution: str = texts.INSTITUTION
    iban: str = texts.IBAN
    bic: str = texts.BIC
    notice: str = texts.NOTICE


@dataclass
class Footer:
    legal: str = texts.FOOTER_LEFT
    legal_right: str = texts.FOOTER_RIGHT


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_title: bool = True
    header_date: bool = True
    middle: bool = True
    middle_holder: bool = True
    middle_account: bool = True
    middle_notice: bool = True
    footer: bool = True
    footer_legal: bool = True
    footer_legal_right: bool = True


@dataclass
class Doc:
    header: Header = field(default_factory=Header)
    card: Card = field(default_factory=Card)
    footer: Footer = field(default_factory=Footer)
    visible: Visible = field(default_factory=Visible)


def from_payload(data: dict | None) -> Doc:
    data = rules.apply_payload(data)
    doc = Doc()
    vis = doc.visible
    vis.header = rules.flag(data, "header")
    vis.header_logo = rules.flag(data, "header_logo")
    vis.header_title = rules.flag(data, "header_title")
    vis.header_date = rules.flag(data, "header_date")
    vis.middle = rules.flag(data, "middle")
    vis.middle_holder = rules.flag(data, "middle_holder")
    vis.middle_account = rules.flag(data, "middle_account")
    vis.middle_notice = rules.flag(data, "middle_notice")
    vis.footer = rules.flag(data, "footer")
    vis.footer_legal = rules.flag(data, "footer_legal")
    vis.footer_legal_right = rules.flag(data, "footer_legal_right")
    mapping = (
        ("header_title_text", doc.header, "title"),
        ("header_date_text", doc.header, "date"),
        ("middle_titulaire_nom", doc.card, "titulaire_nom"),
        ("middle_titulaire_adresse", doc.card, "titulaire_adresse"),
        ("middle_titulaire_ville", doc.card, "titulaire_ville"),
        ("middle_titulaire_pays", doc.card, "titulaire_pays"),
        ("middle_date_ouverture", doc.card, "date_ouverture"),
        ("middle_institution", doc.card, "institution"),
        ("middle_iban_text", doc.card, "iban"),
        ("middle_bic_text", doc.card, "bic"),
        ("middle_notice_text", doc.card, "notice"),
        ("footer_legal_text", doc.footer, "legal"),
        ("footer_legal_right_text", doc.footer, "legal_right"),
    )
    for key, obj, attr in mapping:
        if key in data:
            setattr(obj, attr, data[key])
        elif key == "middle_iban_text" and isinstance(data.get("middle_iban"), str):
            doc.card.iban = data["middle_iban"]
        elif key == "middle_bic_text" and isinstance(data.get("middle_bic"), str):
            doc.card.bic = data["middle_bic"]
    return rules.apply_doc(doc)
