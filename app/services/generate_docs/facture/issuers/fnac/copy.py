from app.services.generate_docs.common import example_dates as _dates

NOM = "Martin"
PRENOM = "Lucas"
CLIENT_NOM = "Martin Lucas"
EMAIL = "martin.lucas@gmail.com"
ADRESSE = "12 Rue des Fleurs"
VILLE = "75011 Paris"
PAYS_WEB = "France Métropolitaine"
PAYS_MAG = ""

STORE_WEB_NOM = "FNAC DIRECT"
STORE_WEB_L1 = "ZONE LOGISTIQUE NORD"
STORE_WEB_L2 = "91000 EVRY"
STORE_WEB_L3 = "FRANCE"

STORE_MAG_NOM = "FNAC Forum"
STORE_MAG_L1 = "Forum des Halles"
STORE_MAG_L2 = "75001 Paris"
STORE_MAG_L3 = ""

NUM_COMMANDE = "BXU7ZFTY2SUE2"
NUM_FACTURE = "2027880107"
NREF = "2027880107 - MLUCAS -FND"


def __getattr__(name: str):
    if name == "DATE_WEB":
        return _dates.fnac_web()
    if name == "DATE_MAG":
        return _dates.fnac_magasin()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
MATRICULE = "7000575"

PAYMENT_WEB = "Carte bancaire"
PAYMENT_MAG = "A la caisse"
PAYMENT_MODES = (
    "Cheque-cadeau",
    "A la caisse",
    "Carte bancaire",
    "Espèces",
    "Chèque",
    "Virement",
    "PayPal",
    "Ticket restaurant",
    "3x sans frais",
)
TVA_CODE_WEB = "I"
TVA_CODE_MAG = "1"
TVA_RATE = "20.00"

LIVRAISON = "Livraison"
FACTURATION = "Facturation"
CMD_WEB = "COMMANDE :"
CMD_MAG = "Commande: N°"
INV_WEB = "FACTURE/INVOICE :"
INV_MAG = "Facture: N°"
DU_WEB = "Du :"
DU_MAG = "du"
MAT_LABEL = "Matricule vendeur:"
NREF_PREFIX = "N/Réf "

COL_TVA = "TVA"
COL_EAN = "EAN"
COL_REF = "Référence"
COL_QTE = "Quantité"
COL_LIB = "Libellé"
COL_HT = "Prix Unitaire Net HT"
COL_TTC = "Prix Unitaire Net TTC"
COL_MT = "Montant Net HT"

SHIP = (
    "Pays d'expédition : FRANCE (Union Européenne) – "
    "Shipping country : FRANCE (European Union)"
)

VAT_CODE = "Code - Taux"
VAT_BASE = "Base march.HT"
VAT_TAX = "Taxes/march."
VAT_FRAIS = "Frais HT"
VAT_FRAIS_TVA = "TVA/Frais"
DFFE = "DFFE"

PAY_TITLE = "Réglement"
PAY_MODE = "Mode"
PAY_MONTANT = "Montant"
ECHEANCE_PREFIX = "Echéance le "

TOT_HT = "Total HT"
TOT_TAX = "Total Taxes"
TOT_GRAND_WEB = "TOTAL GENERAL TTC"
TOT_GRAND_MAG = "TOTAL GENERAL"
EUR = "EUR"

SERIAL_PREFIX = "N° de Série : "
ECO_LABEL = "Eco- Participation DEEE"
REMISE_PREFIX = "Prix Unitaire Brut HT: "
REMISE_MID = "  -  Remise Unitaire HT: "
VOLUME = "Volume"

PAGE_FMT = "Page {current}/{total} Fin"

PILL = "La Fnac à votre écoute"
HELP_WEB_TITLE = "Votre commande Fnac.com :"
HELP_WEB_BODY = (
    "contactez-nous au 0969 324 334 (Service Gratuit + prix appel) "
    "du lundi au samedi de 9h à 19h30"
)
HELP_TECH_TITLE = "Un problème technique :"
HELP_TECH_1 = (
    "pendant la durée de la garantie technique, contactez-nous au "
    "0969 324 334 (Service Gratuit + prix appel) du lundi au samedi "
    "de 8h30 à 21h, les dimanches"
)
HELP_TECH_2 = "et jours fériés de 10h à 18h"

LEGAL_WEB = (
    "Fnac Direct - SAS au capital de 13.583.280 EUR.",
    "9 rue des Bateaux-Lavoirs",
    "94200 Ivry-sur-Seine - FRANCE",
    "R.C.S. Nanterre B 377 853 536 - TVA FR93377853536",
)
LEGAL_MAG = (
    "R.C.S. Nanterre B 377 853 536 - TVA FR93377853536",
)

PRODUIT = "Casque audio sans fil Bluetooth, autonomie 30 h."
SUBTITLE = ""
EAN = "3001100110011"
REFERENCE = "1001101"
QTE = "1"
PU_HT = "100.00"
PU_TTC = "120.00"
PU_BRUT = "120.00"
REMISE_HT = "20.00"
ECO_HT = "0.00"
ECO_TTC = "0.00"
SERIAL = ""
DISTRIBUTION = ""
PIECES = ""
GARANTIE = ""
FRAIS_HT = "0.00"
TVA_FRAIS = "0.00"
