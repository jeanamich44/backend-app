from . import rib

TITLE = "RIB · Relevé d'Identité Bancaire"
INTL_TITLE = "Identifiant international de compte bancaire"

LABEL_TITULAIRE = "Titulaire du compte"
LABEL_DOM = "Domiciliation"
COL_BANQUE = "Code banque"
COL_AGENCE = "Code agence"
COL_COMPTE = "Numéro de compte"
COL_CLE = "Clé RIB"
LABEL_IBAN = "IBAN"
LABEL_BIC = "BIC"

CIVILITE = "M."
NOM = "MARTIN"
PRENOM = "LUCAS"
TITULAIRE_NOM = "MARTIN LUCAS"
TITULAIRE_RUE = "12 Rue Des Fleurs"
TITULAIRE_CP = "75011"
TITULAIRE_VILLE = "Paris"
TITULAIRE_DEPT = "Île-de-France"

DOM_NOM = "Revolut France, succursale de Revolut Bank UAB"
DOM_RUE = "10 avenue Kléber 75116 Paris"
DOM_PAYS = "France"

BANQUE = "28233"
GUICHET = "00001"
COMPTE = "00000012345"
CLE = rib.cle_rib(BANQUE, GUICHET, COMPTE)
IBAN = rib.iban_fr(BANQUE, GUICHET, COMPTE, CLE)
BIC = "REVOFRP2"
