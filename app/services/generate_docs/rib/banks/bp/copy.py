from . import rib

TITLE = "RELEVE D'IDENTITE BANCAIRE"
FOOTER_PAGE = "1 / 1"
FOOTER_RIB = "RIBS0000"

LABEL_DOM = "DOMICILIATION :"
DOMICILIATION = "AG ECO SOCIALE SOLIDAIRE"

COL_BANQUE = "CODE BANQUE"
COL_GUICHET = "CODE GUICHET"
COL_COMPTE = "NUMERO DE COMPTE"
COL_CLE = "CLE RIB"

BANQUE = "18707"
GUICHET = "00656"
COMPTE = "00012345678"
CLE = rib.cle_rib(BANQUE, GUICHET, COMPTE)
IBAN = rib.iban_fr(BANQUE, GUICHET, COMPTE, CLE)
BIC = "CCBPFRPPVER"

LABEL_IBAN = "IBAN :"
LABEL_BIC = "Adresse SWIFT (BIC) :"

LABEL_TITULAIRE = "TITULAIRE DU COMPTE"
LABEL_ADRESSE = "ADRESSE"

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

NOTICE = (
    "Ce relevé d'identité bancaire est à utiliser pour les opérations que vous seriez "
    "amené à inscrire à mon compte ouvert à la BANQUE POPULAIRE VAL DE FRANCE "
    "(virements, versements...)\n"
    "Son utilisation vous garantira le bon enregistrement des opérations en cause "
    "et évitera les retards ou erreurs d'imputation."
)
