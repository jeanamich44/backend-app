from . import rib

TITLE = "Relevé d’Identité Bancaire / Bank details statement"

TEXT = (
    "Ce relevé est destiné à être remis, sur leur demande, à vos créanciers ou "
    "débiteurs appelés à faire inscrire des opérations à votre compte (virements, "
    "paiements de quittances, etc.).\n"
    "Son utilisation vous garantit le bon enregistrement des opérations en cause et "
    "vous évite ainsi des réclamations pour erreurs ou retards d'imputation. / This "
    "statement is intended for your payees and/or payors when setting up Direct "
    "debit, Standing orders, Transfers and Payment. Please use this Bank account "
    "statement when booking transactions. It will help avoiding execution errors "
    "which might result in unnecessary delays."
)

LABEL_TITULAIRE = "Titulaire du compte / Account holder"
TITULAIRE_PREFIX = ""
CIVILITE = "M."
NOM = "MARTIN"
PRENOM = "LUCAS"
TITULAIRE_NOM = "M. MARTIN LUCAS"
TITULAIRE_OPT = ""
ADRESSE = "12 RUE DES FLEURS"
TITULAIRE_RUE = "12 RUE DES FLEURS"
CP = "75011"
VILLE = "PARIS"
TITULAIRE_VILLE = "75011 PARIS"

LABEL_IBAN = "IBAN"
LABEL_BIC = "BIC"

COL_BANQUE = "Code Banque"
COL_GUICHET = "Code guichet"
COL_COMPTE = "N° du compte"
COL_CLE = "Clé RIB"

BANQUE = "17515"
GUICHET = "90000"
COMPTE = "08123456789"
CLE = rib.cle_rib(BANQUE, GUICHET, COMPTE)
IBAN = rib.iban_fr(BANQUE, GUICHET, COMPTE, CLE)
BIC = "CEPAFRPP751"

LABEL_DOM = "Domiciliation / Paying Bank"
DOMICILIATION_RUE = "12 PLACE JEAN JAURES"
DOMICILIATION_CP = "93100"
DOMICILIATION_VILLE = "MONTREUIL"
