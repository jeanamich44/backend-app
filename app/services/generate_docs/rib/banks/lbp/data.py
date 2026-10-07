"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import rules


@dataclass
class Header:
    title: str = texts.TITLE
    notice_fr: str = texts.NOTICE_FR
    notice_en: str = texts.NOTICE_EN


@dataclass
class Card:
    title: str = texts.TITLE
    etablissement: str = texts.ETABLISSEMENT
    guichet: str = texts.GUICHET
    compte: str = texts.COMPTE
    cle: str = texts.CLE
    domiciliation: str = texts.DOMICILIATION
    iban: str = texts.IBAN
    bic: str = texts.BIC
    titulaire_nom: str = texts.TITULAIRE_NOM
    titulaire_opt1: str = texts.TITULAIRE_OPT1
    titulaire_opt2: str = texts.TITULAIRE_OPT2
    titulaire_rue: str = texts.TITULAIRE_RUE
    titulaire_ville: str = texts.TITULAIRE_VILLE

    def titulaire_lines(self) -> tuple:
        ordered = (
            self.titulaire_nom,
            self.titulaire_opt1,
            self.titulaire_opt2,
            self.titulaire_rue,
            self.titulaire_ville,
        )
        lines = tuple(part.strip() for part in ordered if part and str(part).strip())
        return lines[:5]


@dataclass
class Footer:
    line1: str = texts.FOOTER_L1
    line2: str = texts.FOOTER_L2
    code: str = texts.FOOTER_CODE


@dataclass
class Visible:
    header: bool = True
    header_title: bool = True
    header_notice_fr: bool = True
    header_notice_en: bool = True
    middle: bool = True
    middle_logo: bool = True
    middle_title: bool = True
    middle_table: bool = True
    middle_iban_bic: bool = True
    middle_titulaire: bool = True
    middle_separator: bool = True
    footer: bool = True
    footer_mentions: bool = True


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
    vis.header_title = rules.flag(data, "header_title")
    vis.header_notice_fr = rules.flag(data, "header_notice_fr")
    vis.header_notice_en = rules.flag(data, "header_notice_en")
    vis.middle = rules.flag(data, "middle")
    vis.middle_logo = rules.flag(data, "middle_logo")
    vis.middle_title = rules.flag(data, "middle_title")
    vis.middle_table = rules.flag(data, "middle_table")
    vis.middle_iban_bic = rules.flag(data, "middle_iban_bic")
    vis.middle_titulaire = rules.flag(data, "middle_titulaire")
    vis.middle_separator = rules.flag(data, "middle_separator")
    vis.footer = rules.flag(data, "footer")
    vis.footer_mentions = rules.flag(data, "footer_mentions")
    if "header_title_text" in data:
        doc.header.title = data["header_title_text"]
    if "header_notice_fr_text" in data:
        doc.header.notice_fr = data["header_notice_fr_text"]
    if "header_notice_en_text" in data:
        doc.header.notice_en = data["header_notice_en_text"]
    if "middle_title_text" in data:
        doc.card.title = data["middle_title_text"]
    elif isinstance(data.get("header_brand_title_text"), str):
        doc.card.title = data["header_brand_title_text"]
    if "middle_etablissement" in data:
        doc.card.etablissement = data["middle_etablissement"]
    if "middle_guichet" in data:
        doc.card.guichet = data["middle_guichet"]
    if "middle_compte" in data:
        doc.card.compte = data["middle_compte"]
    if "middle_cle" in data:
        doc.card.cle = data["middle_cle"]
    if isinstance(data.get("middle_domiciliation"), str):
        doc.card.domiciliation = data["middle_domiciliation"]
    if isinstance(data.get("middle_iban"), str):
        doc.card.iban = data["middle_iban"]
    if isinstance(data.get("middle_bic"), str):
        doc.card.bic = data["middle_bic"]
    if "middle_titulaire_nom" in data:
        doc.card.titulaire_nom = data["middle_titulaire_nom"]
    if "middle_titulaire_opt1" in data:
        doc.card.titulaire_opt1 = data["middle_titulaire_opt1"]
    if "middle_titulaire_opt2" in data:
        doc.card.titulaire_opt2 = data["middle_titulaire_opt2"]
    if "middle_titulaire_rue" in data:
        doc.card.titulaire_rue = data["middle_titulaire_rue"]
    if "middle_titulaire_ville" in data:
        doc.card.titulaire_ville = data["middle_titulaire_ville"]
    if "footer_line1_text" in data:
        doc.footer.line1 = data["footer_line1_text"]
    if "footer_line2_text" in data:
        doc.footer.line2 = data["footer_line2_text"]
    if "footer_code_text" in data:
        doc.footer.code = data["footer_code_text"]
    return rules.apply_doc(doc)
