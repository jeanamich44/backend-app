"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import rules


@dataclass
class Card:
    civilite: str = "M."
    nom: str = texts.CLIENT_NOM
    adresse: str = texts.ADRESSE
    cp_ville: str = texts.CP_VILLE
    date_facture: str = field(default_factory=texts.slash_date_yy)
    num_facture: str = texts.NUM_FACTURE
    num_client: str = texts.NUM_CLIENT
    num_contrat: str = texts.NUM_CONTRAT
    lieu_pce: str = texts.LIEU_PCE
    lieu_bat: str = texts.LIEU_BAT
    montant_gaz: str = texts.MONTANT_GAZ
    montant_prestations: str = texts.MONTANT_PREST
    total: str = texts.TOTAL_TTC
    montant_ht: str = texts.MONTANT_HT
    montant_tva: str = texts.MONTANT_TVA
    compte: str = texts.COMPTE


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_title: bool = True
    header_refs: bool = True
    header_lieu: bool = True
    header_window: bool = True
    header_barcode: bool = True
    header_correspond: bool = True
    middle: bool = True
    middle_legal: bool = True
    middle_amounts: bool = True
    middle_next: bool = True
    middle_paiement: bool = True
    footer: bool = True
    footer_contacts: bool = True
    footer_economies: bool = True
    footer_cheque: bool = True
    footer_triman: bool = True


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
    vis.header_title = rules.flag(data, "header_title")
    vis.header_refs = rules.flag(data, "header_refs")
    vis.header_lieu = rules.flag(data, "header_lieu")
    vis.header_window = rules.flag(data, "header_window")
    vis.header_barcode = rules.flag(data, "header_barcode")
    vis.header_correspond = rules.flag(data, "header_correspond")
    vis.middle = rules.flag(data, "middle")
    vis.middle_legal = rules.flag(data, "middle_legal")
    vis.middle_amounts = rules.flag(data, "middle_amounts")
    vis.middle_next = rules.flag(data, "middle_next")
    vis.middle_paiement = rules.flag(data, "middle_paiement")
    vis.footer = rules.flag(data, "footer")
    vis.footer_contacts = rules.flag(data, "footer_contacts")
    vis.footer_economies = rules.flag(data, "footer_economies")
    vis.footer_cheque = rules.flag(data, "footer_cheque")
    vis.footer_triman = rules.flag(data, "footer_triman")
    for key in rules.FIELDS:
        if key in data:
            setattr(doc.card, key, data[key])
    return rules.apply_doc(doc)
