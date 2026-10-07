from app.services.generate_docs.common import example_dates as _dates

TITLE = "DÉCLARATION D'EXPÉDITION"

SERVICE_LINES = (
    "Service Client",
    "T +44 (0)20 3402 1444",
    "E customerservice@burberry.com",
)

NUM_LABEL = "NUMÉRO DE COMMANDE"
DATE_ORDER_LABEL = "DATE DE LA "
DATE_ORDER_LABEL2 = "COMMANDE"
DATE_SHIP_LABEL = "DATE D'EXPÉDITION"
COLLECT = "COLLECT-IN-STORE"

SHIP_TITLE = "ADRESSE D'EXPÉDITION"
BILL_TITLE = "ADRESSE DE FACTURATION"

STORE_ADRESSE = "65 Rue du Faubourg St-Honore"
STORE_VILLE = "Paris"
STORE_CP = "75008"
STORE_PAYS = "France"

NOM = "Martin"
PRENOM = "Lucas"
CLIENT_NOM = "Martin Lucas"
ADRESSE = "12 Rue des Fleurs"
VILLE = "Paris"
CP = "75011"
PAYS = "France"

NUM_COMMANDE = "4845001"

COL_ITEM = "Item"
COL_SKU = "N° d'article"
COL_CODE_L1 = "CODE  À"
COL_CODE_L2 = "BARRES"
COL_DESC = "DESCRIPTION"
COL_SIZE = "TAILLE"
COL_COLOR = "COULEUR"
COL_QTY = "QTÉ"
COL_PRICE = "PRIX"
COLLECT_ROW = "COLLECT AT STORE"
TOTAL_LABEL = "PRIX TOTAL"

SKU = "80089081003"
BARCODE = "5045556761666"
DESC = "Cotton Pique Polo"
DESC2 = "Polo Shirt"
TAILLE = "M"
COULEUR = "Noir"
QTE = "1"
PRIX = "80.00"

PAY_LABEL = "MÉTHODE DE PAIEMENT"
PAY_WITH = "Payé avec"
PAY_THANKS = "Merci"
PAYMENT = "MasterCard *************6357"
PAYMENT_MODES = (
    "MasterCard *************6357",
    "Visa *************6357",
    "American Express *************6357",
    "PayPal",
    "Apple Pay",
    "Carte cadeau",
    "Virement",
)

NOTICE = "Prenez soin de remplir la section Récupération de la commande au dos."

LEGAL = (
    "BURBERRY GROUP PLC, HORSEPERRY HOUSE HORSEPERRY ROAD, LONDON SW1P 2AW +44 (0)20 3067 3000 BURBERRY.COM",
    "REGISTERED IN ENGLAND WALES NUMBER: 03438224 REGISTERED OFFICE: HORSEPERRY HOUS, HORSPERRY ROAD, LONDON, SW1p 2AW",
)


def slash_date(d=None) -> str:
    return _dates.burberry_order(d)
