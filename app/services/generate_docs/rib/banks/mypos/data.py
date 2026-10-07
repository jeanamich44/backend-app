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
    nom_societe: str = texts.NOM_SOCIETE
    num_enregistrement: str = texts.NUM_ENREGISTREMENT
    adresse: str = texts.ADRESSE
    cp_ville: str = texts.CP_VILLE
    pays: str = texts.PAYS
    titulaire: str = texts.TITULAIRE
    compte: str = texts.COMPTE
    iban: str = texts.IBAN
    bic: str = texts.BIC
    devise: str = texts.DEVISE


@dataclass
class Footer:
    page: str = texts.PAGE_NO


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_title: bool = True
    header_date: bool = True
    header_address: bool = True
    middle: bool = True
    middle_letter: bool = True
    middle_table: bool = True
    footer: bool = True
    footer_legal: bool = True
    footer_page: bool = True


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
    vis.header_address = rules.flag(data, "header_address")
    vis.middle = rules.flag(data, "middle")
    vis.middle_letter = rules.flag(data, "middle_letter")
    vis.middle_table = rules.flag(data, "middle_table")
    vis.footer = rules.flag(data, "footer")
    vis.footer_legal = rules.flag(data, "footer_legal")
    vis.footer_page = rules.flag(data, "footer_page")
    mapping = (
        ("header_title_text", doc.header, "title"),
        ("header_date_text", doc.header, "date"),
        ("middle_nom_societe", doc.card, "nom_societe"),
        ("middle_num_enregistrement", doc.card, "num_enregistrement"),
        ("middle_adresse", doc.card, "adresse"),
        ("middle_cp_ville", doc.card, "cp_ville"),
        ("middle_pays", doc.card, "pays"),
        ("middle_titulaire_nom", doc.card, "titulaire"),
        ("middle_compte", doc.card, "compte"),
        ("middle_iban_text", doc.card, "iban"),
        ("middle_bic_text", doc.card, "bic"),
        ("middle_devise", doc.card, "devise"),
        ("footer_page_text", doc.footer, "page"),
    )
    for key, obj, attr in mapping:
        if key in data:
            setattr(obj, attr, data[key])
        elif key == "middle_iban_text" and isinstance(data.get("middle_iban"), str):
            doc.card.iban = data["middle_iban"]
        elif key == "middle_bic_text" and isinstance(data.get("middle_bic"), str):
            doc.card.bic = data["middle_bic"]
    return rules.apply_doc(doc)
