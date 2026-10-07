"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import rules


@dataclass
class Header:
    title: str = texts.TITLE
    crumb: str = texts.CRUMB
    crumb_link: str = texts.CRUMB_LINK


@dataclass
class Card:
    notice: str = texts.NOTICE
    caisse: str = texts.CAISSE
    agence: str = texts.AGENCE
    tel: str = texts.TEL
    fax: str = texts.FAX
    date: str = field(default_factory=lambda: texts.DATE)
    code: str = texts.CODE
    titulaire_nom: str = texts.TITULAIRE_NOM
    titulaire_opt: str = texts.TITULAIRE_OPT
    titulaire_rue: str = texts.TITULAIRE_RUE
    titulaire_ville: str = texts.TITULAIRE_VILLE
    domiciliation: str = texts.DOMICILIATION
    banque: str = texts.BANQUE
    guichet: str = texts.GUICHET
    compte: str = texts.COMPTE
    cle: str = texts.CLE
    iban: str = texts.IBAN
    bic: str = texts.BIC


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_title: bool = True
    header_crumb: bool = True
    middle: bool = True
    middle_notice: bool = True
    middle_lines: bool = True
    middle_agence: bool = True
    middle_titulaire: bool = True
    middle_domiciliation: bool = True
    middle_table: bool = True
    middle_iban: bool = True
    middle_bic: bool = True
    footer: bool = True


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
    vis.header_crumb = rules.flag(data, "header_crumb")
    vis.middle = rules.flag(data, "middle")
    vis.middle_notice = rules.flag(data, "middle_notice")
    vis.middle_lines = rules.flag(data, "middle_lines")
    vis.middle_agence = rules.flag(data, "middle_agence")
    vis.middle_titulaire = rules.flag(data, "middle_titulaire")
    vis.middle_domiciliation = rules.flag(data, "middle_domiciliation")
    vis.middle_table = rules.flag(data, "middle_table")
    vis.middle_iban = rules.flag(data, "middle_iban")
    vis.middle_bic = rules.flag(data, "middle_bic")
    vis.footer = rules.flag(data, "footer")
    if "header_title_text" in data:
        doc.header.title = data["header_title_text"]
    if "header_crumb_text" in data:
        doc.header.crumb = data["header_crumb_text"]
    if "header_crumb_link" in data:
        doc.header.crumb_link = data["header_crumb_link"]
    if "middle_notice_text" in data:
        doc.card.notice = data["middle_notice_text"]
    elif isinstance(data.get("middle_notice"), str):
        doc.card.notice = data["middle_notice"]
    if "middle_caisse" in data:
        doc.card.caisse = data["middle_caisse"]
    if "middle_agence_ville" in data:
        doc.card.agence = data["middle_agence_ville"]
    if "middle_tel" in data:
        doc.card.tel = data["middle_tel"]
    if "middle_fax" in data:
        doc.card.fax = data["middle_fax"]
    if "middle_date" in data:
        doc.card.date = data["middle_date"]
    if "middle_code" in data:
        doc.card.code = data["middle_code"]
    if "middle_titulaire_nom" in data:
        doc.card.titulaire_nom = data["middle_titulaire_nom"]
    if "middle_titulaire_opt" in data:
        doc.card.titulaire_opt = data["middle_titulaire_opt"]
    if "middle_titulaire_rue" in data:
        doc.card.titulaire_rue = data["middle_titulaire_rue"]
    if "middle_titulaire_ville" in data:
        doc.card.titulaire_ville = data["middle_titulaire_ville"]
    if "middle_domiciliation_text" in data:
        doc.card.domiciliation = data["middle_domiciliation_text"]
    elif isinstance(data.get("middle_domiciliation"), str):
        doc.card.domiciliation = data["middle_domiciliation"]
    if "middle_banque" in data:
        doc.card.banque = data["middle_banque"]
    if "middle_guichet" in data:
        doc.card.guichet = data["middle_guichet"]
    if "middle_compte" in data:
        doc.card.compte = data["middle_compte"]
    if "middle_cle" in data:
        doc.card.cle = data["middle_cle"]
    if "middle_iban_text" in data:
        doc.card.iban = data["middle_iban_text"]
    elif isinstance(data.get("middle_iban"), str):
        doc.card.iban = data["middle_iban"]
    if "middle_bic_text" in data:
        doc.card.bic = data["middle_bic_text"]
    elif isinstance(data.get("middle_bic"), str):
        doc.card.bic = data["middle_bic"]
    return rules.apply_doc(doc)
