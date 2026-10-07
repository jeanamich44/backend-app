from . import rib

TITLE = "Relevé d'Identité Bancaire / IBAN"

CIVILITE = "M."
NOM = "MARTIN"
PRENOM = "LUCAS"
TITULAIRE_NOM = "M. MARTIN LUCAS"
ADRESSE = "12 RUE DES FLEURS"
TITULAIRE_RUE = "12 RUE DES FLEURS"
CP = "75011"
VILLE = "PARIS"
TITULAIRE_VILLE = "75011 PARIS"

BANQUE = "30004"
GUICHET = "01852"
COMPTE = "00020034567"
CLE = rib.cle_rib(BANQUE, GUICHET, COMPTE)
IBAN = rib.iban_fr(BANQUE, GUICHET, COMPTE, CLE)
BIC = "BNPAFRPPXXX"
DOMICILIATION = "BNPPARB LYON BROTTEAUX (00120)"

LABEL_IBAN = "IBAN    :"
LABEL_BIC = "BIC    :"
LABEL_RIB = "RIB    :"
REF_1 = "(1)"
REF_2 = "(2)"
REF_3 = "(3)"

COL_BANQUE = "Code banque"
COL_AGENCE = "Code agence"
COL_COMPTE = "Numéro de compte"
COL_CLE = "Clé RIB"
COL_DOM = "Agence de domiciliation"

LEGEND_IBAN = "International Bank Account Number"
LEGEND_BIC = "Bank Identifier Code"
LEGEND_RIB = "Relevé d'Identité Bancaire"
