from . import rib

TITLE = "RELEVE D'IDENTITE BANCAIRE"

NOTICE_FR = (
    "Ce relevé est destiné à être remis, sur leur demande, à vos créanciers "
    "ou débiteurs appelés à faire inscrire des opérations à votre compte "
    "(virements, prélèvements, etc.)."
)
NOTICE_EN = (
    "This statement is intended to be delivered to those of your creditors "
    "or debitors who have transactions posted to your account "
    "(credit transferts, invoice payments, etc.)."
)
NOTICE = NOTICE_FR + "\n" + NOTICE_EN

NAT_TITLE = "IDENTIFICATION NATIONALE / DOMESTIC IDENTIFICATION"
INTL_TITLE = "IDENTIFICATION INTERNATIONALE / INTERNATIONAL IDENTIFICATION"

COL_BANQUE = "Code Banque"
COL_GUICHET = "Indicatif"
COL_COMPTE = "Numéro de compte"
COL_CLE = "Clé RIB"
COL_DOM = "Domiciliation"
LABEL_IBAN = "IBAN"
LABEL_BIC = "BIC / Adresse Swift"
LABEL_TITULAIRE = "TITULAIRE DU COMPTE\xa0: "
LIBELLE = "Libellé complémentaire:"

CIVILITE = "M."
NOM = "MARTIN"
PRENOM = "LUCAS"
TITULAIRE_NOM = "M. MARTIN LUCAS"
ADRESSE = "12 RUE DES FLEURS"
TITULAIRE_RUE = "12 RUE DES FLEURS"
CP = "75011"
VILLE = "PARIS"
TITULAIRE_VILLE = "75011 PARIS"

BANQUE = "30002"
GUICHET = "00001"
COMPTE = "00000012345"
CLE = rib.cle_rib(BANQUE, GUICHET, COMPTE)
IBAN = rib.iban_fr(BANQUE, GUICHET, COMPTE, CLE)
BIC = "CRLYFRPPXXX"
DOMICILIATION = "RGPNO PARIS BATIGNOLLES"
