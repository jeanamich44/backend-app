"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import rules


@dataclass
class Header:
    title: str = texts.TITLE


@dataclass
class Card:
    banque: str = texts.BANQUE
    guichet: str = texts.GUICHET
    compte: str = texts.COMPTE
    cle: str = texts.CLE
    iban: str = texts.IBAN
    bic: str = texts.BIC
    domiciliation: str = texts.DOMICILIATION
    titulaire_nom: str = texts.TITULAIRE_NOM
    notice: str = texts.NOTICE


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_title: bool = True
    middle: bool = True
    middle_notice: bool = True
    middle_titulaire: bool = True
    middle_iban: bool = True
    middle_bic: bool = True
    middle_domiciliation: bool = True
    middle_table: bool = True
    middle_libelle: bool = True
    middle_lines: bool = True


@dataclass
class Doc:
    header: Header = field(default_factory=Header)
    card: Card = field(default_factory=Card)
    visible: Visible = field(default_factory=Visible)


def from_payload(data: dict | None) -> Doc:
    data = rules.apply_payload(data)
    doc = Doc()
    vis = doc.visible
    vis.header = rules.flag(data, "header")
    vis.header_logo = rules.flag(data, "header_logo")
    vis.header_title = rules.flag(data, "header_title")
    vis.middle = rules.flag(data, "middle")
    vis.middle_notice = rules.flag(data, "middle_notice")
    vis.middle_titulaire = rules.flag(data, "middle_titulaire")
    vis.middle_iban = rules.flag(data, "middle_iban")
    vis.middle_bic = rules.flag(data, "middle_bic")
    vis.middle_domiciliation = rules.flag(data, "middle_domiciliation")
    vis.middle_table = rules.flag(data, "middle_table")
    vis.middle_libelle = rules.flag(data, "middle_libelle")
    vis.middle_lines = rules.flag(data, "middle_lines")
    if "header_title_text" in data:
        doc.header.title = data["header_title_text"]
    if "middle_notice_text" in data:
        doc.card.notice = data["middle_notice_text"]
    if "middle_titulaire_nom" in data:
        doc.card.titulaire_nom = data["middle_titulaire_nom"]
    if "middle_iban_text" in data:
        doc.card.iban = data["middle_iban_text"]
    elif isinstance(data.get("middle_iban"), str):
        doc.card.iban = data["middle_iban"]
    if "middle_bic_text" in data:
        doc.card.bic = data["middle_bic_text"]
    elif isinstance(data.get("middle_bic"), str):
        doc.card.bic = data["middle_bic"]
    if "middle_domiciliation_text" in data:
        doc.card.domiciliation = data["middle_domiciliation_text"]
    if "middle_banque" in data:
        doc.card.banque = data["middle_banque"]
    if "middle_guichet" in data:
        doc.card.guichet = data["middle_guichet"]
    if "middle_compte" in data:
        doc.card.compte = data["middle_compte"]
    if "middle_cle" in data:
        doc.card.cle = data["middle_cle"]
    return rules.apply_doc(doc)
