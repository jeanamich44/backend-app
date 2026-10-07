from . import rib

TITLE = "Coordonnées bancaires"
ACCOUNT_PREFIX = "Nom du compte : "
ACCOUNT_NAME = "Compte Principal"

LABEL_IBAN = "IBAN"
LABEL_BIC = "BIC/SWIFT"
LABEL_TITULAIRE = "Titulaire"
LABEL_BANQUE = "Banque"
LABEL_AGENCE = "Agence"
LABEL_COMPTE = "Compte"
LABEL_CLE = "Clé"

CIVILITE = "M."
NOM = "MARTIN"
PRENOM = "LUCAS"
TITULAIRE_NOM = "MARTIN LUCAS"
ADRESSE = "12 RUE DES FLEURS"
TITULAIRE_RUE = "12 RUE DES FLEURS"
CP = "75011"
VILLE = "PARIS"
TITULAIRE_VILLE = "75011 PARIS"

DOMICILIATION = (
    "Domiciliation: Qonto (Olinda SAS), 18 rue de Navarin, 75009 Paris, France"
)

SWIFT_BADGE = "SWIFT"
SWIFT_L1 = "La banque émettrice pourrait vous"
SWIFT_L2 = "demander le BIC de notre banque"
SWIFT_L3 = "partenaire avant d'effectuer un virement"
SWIFT_L4_PREFIX = "SWIFT : "
SWIFT_L4_CODE = "TRWIBEB3XXX"
SWIFT_L4_DOT = "."

BANQUE = "16958"
GUICHET = "00001"
COMPTE = "00012345678"
CLE = rib.cle_rib(BANQUE, GUICHET, COMPTE)
IBAN = rib.iban_fr(BANQUE, GUICHET, COMPTE, CLE)
BIC = "QNTOFRP1XXX"
