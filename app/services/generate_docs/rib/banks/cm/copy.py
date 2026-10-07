from . import rib

TITLE = "RELEVE D’IDENTITE BANCAIRE"

LABEL_RIB = "Identifiant national de compte bancaire - RIB"
COL_BANQUE = "Banque"
COL_GUICHET = "Guichet"
COL_COMPTE = "N° compte"
COL_CLE = "Clé"
COL_DEVISE = "Devise"

BANQUE = "10278"
GUICHET = "00001"
COMPTE = "00012345678"
CLE = rib.cle_rib(BANQUE, GUICHET, COMPTE)
DEVISE = "EUR"

LABEL_AGENCE = "Domiciliation"
AGENCE = "CM PARIS CENTRE"

LABEL_IBAN_HEAD = "Identifiant international de compte bancaire"
LABEL_IBAN = "IBAN (International Bank Account Number)"
IBAN = rib.iban_fr(BANQUE, GUICHET, COMPTE, CLE)
LABEL_BIC = "BIC (Bank Identifier Code)"
BIC = "CMCIFRPP"

LABEL_DOM = "Domiciliation"
DOMICILIATION_RUE = "15 RUE DE LA PAIX"
DOMICILIATION_CP = "75002"
DOMICILIATION_VILLE = "PARIS"
PHONE = "0100000000"

LABEL_TITULAIRE = "Titulaire du compte (Account Owner)"
CIVILITE = "M."
NOM = "MARTIN"
PRENOM = "LUCAS"
TITULAIRE_NOM = "M. MARTIN LUCAS"
ADRESSE = "12 RUE DES FLEURS"
TITULAIRE_RUE = "12 RUE DES FLEURS"
CP = "75011"
VILLE = "PARIS"
TITULAIRE_VILLE = "75011 PARIS"

NOTICE = (
    "Remettez ce relevé à tout autre organisme ayant besoin de connaître "
    "vos références bancaires pour la domiciliation de vos virements ou de "
    "prélèvements à votre compte. Vous éviterez ainsi des erreurs ou des "
    "retards d’exécution."
)

RESERVED = "PARTIE RESERVEE AU DESTINATAIRE DU RELEVE"


def format_phone(raw: str) -> str:
    digits = "".join(ch for ch in (raw or "") if ch.isdigit())
    if len(digits) == 10:
        grouped = " ".join(digits[i : i + 2] for i in range(0, 10, 2))
        return f" {grouped} "
    if not digits:
        return ""
    return f" {digits} "
