"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import rules


@dataclass
class Card:
    civilite: str = texts.CIVILITY.strip()
    nom: str = texts.NOM_COMPLET
    prenom: str = ""
    adresse: str = texts.ADRESSE
    cp: str = texts.CP
    ville: str = texts.VILLE
    cp_ville: str = texts.CP_VILLE
    date: str = field(default_factory=texts.paris_date)
    num_client: str = texts.NUM_CLIENT
    depuis: str = texts.DEPUIS


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_window: bool = True
    header_title: bool = True
    middle: bool = True
    middle_refs: bool = True
    middle_body: bool = True
    middle_sign: bool = True
    middle_note: bool = True
    footer: bool = True
    footer_site: bool = True
    footer_legal: bool = True
    footer_ref: bool = True


@dataclass
class Doc:
    card: Card = field(default_factory=Card)
    visible: Visible = field(default_factory=Visible)


def from_payload(data: dict | None) -> Doc:
    data = rules.apply_payload(data)
    doc = Doc()
    vis = doc.visible
    vis.header = rules.flag(data, "header")
    vis.header_logo = rules.flag(data, "header_logo")
    vis.header_window = rules.flag(data, "header_window")
    vis.header_title = rules.flag(data, "header_title")
    vis.middle = rules.flag(data, "middle")
    vis.middle_refs = rules.flag(data, "middle_refs")
    vis.middle_body = rules.flag(data, "middle_body")
    vis.middle_sign = rules.flag(data, "middle_sign")
    vis.middle_note = rules.flag(data, "middle_note")
    vis.footer = rules.flag(data, "footer")
    vis.footer_site = rules.flag(data, "footer_site")
    vis.footer_legal = rules.flag(data, "footer_legal")
    vis.footer_ref = rules.flag(data, "footer_ref")
    for key in rules.FIELDS:
        if key in data:
            setattr(doc.card, key, data[key])
    return rules.apply_doc(doc)
