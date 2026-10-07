"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import rules


@dataclass
class Header:
    title: str = texts.TITLE


@dataclass
class Card:
    titulaire_nom: str = texts.TITULAIRE_NOM
    titulaire_rue: str = texts.TITULAIRE_RUE
    titulaire_cp: str = texts.TITULAIRE_CP
    titulaire_ville: str = texts.TITULAIRE_VILLE
    titulaire_dept: str = texts.TITULAIRE_DEPT
    banque: str = texts.BANQUE
    guichet: str = texts.GUICHET
    compte: str = texts.COMPTE
    cle: str = texts.CLE
    iban: str = texts.IBAN
    bic: str = texts.BIC
    domiciliation_nom: str = texts.DOM_NOM
    domiciliation_rue: str = texts.DOM_RUE
    domiciliation_pays: str = texts.DOM_PAYS


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_title: bool = True
    middle: bool = True
    middle_titulaire: bool = True
    middle_domiciliation: bool = True
    middle_table: bool = True
    middle_iban: bool = True
    middle_bic: bool = True
    middle_lines: bool = True
    middle_separator: bool = True


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
    vis.middle_titulaire = rules.flag(data, "middle_titulaire")
    vis.middle_domiciliation = rules.flag(data, "middle_domiciliation")
    vis.middle_table = rules.flag(data, "middle_table")
    vis.middle_iban = rules.flag(data, "middle_iban")
    vis.middle_bic = rules.flag(data, "middle_bic")
    vis.middle_lines = rules.flag(data, "middle_lines")
    vis.middle_separator = rules.flag(data, "middle_separator")
    mapping = (
        ("header_title_text", doc.header, "title"),
        ("middle_titulaire_nom", doc.card, "titulaire_nom"),
        ("middle_titulaire_rue", doc.card, "titulaire_rue"),
        ("middle_titulaire_cp", doc.card, "titulaire_cp"),
        ("middle_titulaire_ville", doc.card, "titulaire_ville"),
        ("middle_titulaire_dept", doc.card, "titulaire_dept"),
        ("middle_banque", doc.card, "banque"),
        ("middle_guichet", doc.card, "guichet"),
        ("middle_compte", doc.card, "compte"),
        ("middle_cle", doc.card, "cle"),
        ("middle_iban_text", doc.card, "iban"),
        ("middle_bic_text", doc.card, "bic"),
        ("middle_domiciliation_nom", doc.card, "domiciliation_nom"),
        ("middle_domiciliation_rue", doc.card, "domiciliation_rue"),
        ("middle_domiciliation_pays", doc.card, "domiciliation_pays"),
    )
    for key, obj, attr in mapping:
        if key in data:
            setattr(obj, attr, data[key])
        elif key == "middle_iban_text" and isinstance(data.get("middle_iban"), str):
            doc.card.iban = data["middle_iban"]
        elif key == "middle_bic_text" and isinstance(data.get("middle_bic"), str):
            doc.card.bic = data["middle_bic"]
    return rules.apply_doc(doc)
