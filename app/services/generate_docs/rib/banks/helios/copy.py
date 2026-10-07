from . import rib

TITLE = "RELEVÉ D’IDENTITÉ BANCAIRE"

NOTICE = (
    "Ce relevé est destiné à tout organisme ayant besoin de connaître "
    "vos références bancaires pour la domiciliation de vos virements ou "
    "de prélèvements à votre compte. Son utilisation vous permet d'éviter "
    "des erreurs ou des retards d'exécution."
)

CIVILITE = "Mr"
NOM = "MARTIN"
PRENOM = "LUCAS"
TITULAIRE_NOM = "Mr MARTIN LUCAS"
ADRESSE = "12 RUE DES FLEURS"
CP = "75011"
VILLE = "PARIS"
TITULAIRE_ADRESSE = "12 RUE DES FLEURS, 75011 PARIS"

INTL_TITLE = "IDENTIFICATION INTERNATIONALE"
LABEL_IBAN = "IBAN"
LABEL_BIC = "BIC"
LABEL_DOM = "Domiciliation :"
SUP_IBAN = "(1)"
SUP_BIC = "(2)"
SUP_RIB = "(3)"
COLON = " :"

BANQUE = "17448"
GUICHET = "00001"
COMPTE = "00012345678"
CLE = rib.cle_rib(BANQUE, GUICHET, COMPTE)
IBAN = rib.iban_fr(BANQUE, GUICHET, COMPTE, CLE)
BIC = "SFPEFRP2XXX"
DOMICILIATION = "Okali, 50 rue La Boétie, 75008 Paris"

RIB_TITLE = "RIB"
COL_BANQUE = "Code établissement"
COL_GUICHET = "Code guichet"
COL_COMPTE = "Numéro de compte"
COL_CLE = "Clé RIB"

NOTE1 = "(1) International Bank Account Number"
NOTE2 = "(2) Bank Identifier Code"
NOTE3 = "(3) Relevé d'Identité Bancaire"

LEGAL = (
    "HELIOS SAS est une société à mission au capital social de 25 858,80 €, "
    "immatriculée au R.C.S. de Paris sous le numéro 883 111\n"
    "585, et dont le siège social est situé au 9 rue des Colonnes, 75002 Paris. "
    "HELIOS SAS est enregistré sous le numéro REGAFI 731225\n"
    "en tant qu’agent prestataire de services de paiement d'OKALI, établissement "
    "de monnaie électronique agréé et supervisé par l'ACPR,\n"
    "immatriculé au R.C.S. de Paris sous le numéro 827 899 39, et dont le siège "
    "social est situé au 50 rue La Boétie, 75008 Paris. CIB :\n"
    "17448. REGAFI : 91091."
)
