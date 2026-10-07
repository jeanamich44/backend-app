"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import rules


@dataclass
class Card:
    civilite: str = texts.CIVILITE
    nom: str = texts.NOM_COMPLET
    prenom: str = ""
    adresse: str = texts.ADRESSE
    ville: str = texts.VILLE
    cp: str = texts.CP
    num_client: str = texts.NUM_CLIENT
    num_compte: str = texts.NUM_COMPTE
    pdl: str = texts.PDL
    puissance: str = texts.PUISSANCE
    date: str = field(default_factory=texts.today_date)
    contact_titre: str = texts.CONTACT_TITRE
    client_side_libelle: str = texts.CLIENT_SIDE_LIBELLE
    par_internet: str = texts.PAR_INTERNET
    site: str = texts.SITE
    app_mobile: str = texts.APP_MOBILE
    app_nom: str = texts.APP_NOM
    mail_libelle: str = texts.MAIL_LIBELLE
    email: str = texts.EMAIL
    par_telephone: str = texts.PAR_TELEPHONE
    horaires: str = texts.HORAIRES
    num_court: str = texts.NUM_COURT
    service_appel: str = texts.SERVICE_APPEL
    serveur_vocal: str = texts.SERVEUR_VOCAL
    num_vocal: str = texts.NUM_VOCAL
    prix_appel: str = texts.PRIX_APPEL
    par_courrier: str = texts.PAR_COURRIER
    courrier_l1: str = texts.COURRIER_L1
    courrier_l2: str = texts.COURRIER_L2
    courrier_l3: str = texts.COURRIER_L3
    cheque_titre: str = texts.CHEQUE_TITRE
    cheque_courrier: str = texts.CHEQUE_COURRIER
    cheque_l1: str = texts.CHEQUE_L1
    cheque_l2: str = texts.CHEQUE_L2
    lieu_titre: str = texts.LIEU_TITRE
    titulaire_libelle: str = texts.TITULAIRE_LIBELLE
    contrat_libelle: str = texts.CONTRAT_LIBELLE
    n_client_libelle: str = texts.N_CLIENT_LIBELLE
    n_compte_libelle: str = texts.N_COMPTE_LIBELLE
    compte_hint1: str = texts.COMPTE_HINT1
    compte_hint2: str = texts.COMPTE_HINT2
    tarif_bleu: str = texts.TARIF_BLEU
    pdl_libelle: str = texts.PDL_LIBELLE
    n_pdl: str = texts.N_PDL
    puissance_libelle: str = texts.PUISSANCE_LIBELLE
    unite_kva: str = texts.UNITE_KVA
    pour_servir: str = texts.POUR_SERVIR
    cachet_l1: str = texts.CACHET_L1
    cachet_l2: str = texts.CACHET_L2
    cachet_l3: str = texts.CACHET_L3
    conseillere: str = texts.CONSEILLERE
    conseillere_libelle: str = texts.CONSEILLERE_LIBELLE


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_window: bool = True
    header_title: bool = True
    header_contact: bool = True
    middle: bool = True
    middle_body: bool = True
    middle_lieu: bool = True
    middle_date: bool = True
    footer: bool = True
    footer_legal: bool = True
    footer_cachet: bool = False


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
    vis.header_contact = rules.flag(data, "header_contact")
    vis.middle = rules.flag(data, "middle")
    vis.middle_body = rules.flag(data, "middle_body")
    vis.middle_lieu = rules.flag(data, "middle_lieu")
    vis.middle_date = rules.flag(data, "middle_date")
    vis.footer = rules.flag(data, "footer")
    vis.footer_legal = rules.flag(data, "footer_legal")
    vis.footer_cachet = rules.flag(data, "footer_cachet", False)
    for key in rules.FIELDS:
        if key in data:
            setattr(doc.card, key, data[key])
    return rules.apply_doc(doc)
