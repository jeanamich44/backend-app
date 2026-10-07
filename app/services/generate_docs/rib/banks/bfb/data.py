"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import rules


@dataclass
class Header:
    rue: str = texts.RUE
    ville: str = texts.VILLE
    pays: str = texts.PAYS


@dataclass
class Card:
    titulaire_nom: str = texts.TITULAIRE_NOM
    banque: str = texts.BANQUE
    guichet: str = texts.GUICHET
    compte: str = texts.COMPTE
    cle: str = texts.CLE
    iban: str = texts.IBAN
    bic: str = texts.BIC
    domiciliation: str = texts.DOMICILIATION


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_adresse: bool = True
    header_title: bool = True
    middle: bool = True
    middle_card: bool = True
    middle_titulaire: bool = True
    middle_iban: bool = True
    middle_bic: bool = True
    middle_table: bool = True
    middle_domiciliation: bool = True
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
    vis.header_adresse = rules.flag(data, "header_adresse")
    vis.header_title = rules.flag(data, "header_title")
    vis.middle = rules.flag(data, "middle")
    vis.middle_card = rules.flag(data, "middle_card")
    vis.middle_titulaire = rules.flag(data, "middle_titulaire")
    vis.middle_iban = rules.flag(data, "middle_iban")
    vis.middle_bic = rules.flag(data, "middle_bic")
    vis.middle_table = rules.flag(data, "middle_table")
    vis.middle_domiciliation = rules.flag(data, "middle_domiciliation")
    vis.footer = rules.flag(data, "footer")
    if "header_rue" in data:
        doc.header.rue = data["header_rue"]
    if "header_ville" in data:
        doc.header.ville = data["header_ville"]
    if "header_pays" in data:
        doc.header.pays = data["header_pays"]
    if "middle_titulaire_nom" in data:
        doc.card.titulaire_nom = data["middle_titulaire_nom"]
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
    if "middle_domiciliation_text" in data:
        doc.card.domiciliation = data["middle_domiciliation_text"]
    elif isinstance(data.get("middle_domiciliation"), str):
        doc.card.domiciliation = data["middle_domiciliation"]
    return rules.apply_doc(doc)
