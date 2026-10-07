from . import rib

TITLE = "RELEVÉ D'IDENTITÉ BANCAIRE"

NOTICE_FR = (
    "Ce relevé est destiné à être remis, sur demande de vos créanciers et débiteurs, "
    "français ou étrangers appelés à faire inscrire des opérations sur votre compte "
    "(virements, prélèvements...). Nous vous rappelons que les informations contenues "
    "dans votre RIB/IBAN sont de nature confidentielle, c'est pourquoi nous vous invitons "
    "à la plus grande vigilance avant leur transmission."
)

NOTICE_EN = (
    "We remind you that the information contained in your RIB/IBAN is on confidential "
    "nature, and we thus strongly encourage you to be vigilant as regards its transmission."
)

FOOTER_L1 = (
    "La Banque Postale - S.A. à Directoire et Conseil de Surveillance - "
    "Capital Social 6 585 350 218 € - 115 rue de Sèvres 75275 Paris CEDEX 06 - "
)
FOOTER_L2 = "RCS Paris 421 100 645 - IDU EMP FR231771_01UJPN - ORIAS n°07 023 424."
FOOTER_CODE = "Q4X_T00063"

TABLE_TITLE = "RIB - Identifiant national de compte"
COL_ETABLISSEMENT = "ÉTABLISSEMENT"
COL_GUICHET = "GUICHET"
COL_COMPTE = "N° COMPTE"
COL_CLE = "CLÉ RIB"
COL_DOMICILIATION = "DOMICILIATION"
IBAN_TITLE = "IBAN - Identifiant international de compte"
BIC_TITLE = "BIC - Identifiant international de l'établissement"
TITULAIRE_TITLE = "Titulaire du compte"

ETABLISSEMENT = "20041"
GUICHET = "00001"
COMPTE = "3128476M014"
CLE = rib.cle_rib(ETABLISSEMENT, GUICHET, COMPTE)
IBAN = rib.iban_fr(ETABLISSEMENT, GUICHET, COMPTE, CLE)
BIC = "PSSTFRPPPAR"
DOMICILIATION = "LA BANQUE POSTALE PARIS IDF CENTRE FINANCIER"

CIVILITE = "MR"
NOM = "MARTIN"
PRENOM = "LUCAS"
TITULAIRE_NOM = "M. MARTIN LUCAS"
TITULAIRE_OPT1 = "RESIDENCE LES TILLEULS"
TITULAIRE_OPT2 = "BATIMENT B"
TITULAIRE_RUE = "12 RUE DES FLEURS"
CP = "75011"
VILLE = "PARIS"
TITULAIRE_VILLE = "75011 PARIS"
PAYS = "FRANCE"
