from app.services.generate_docs.common import example_dates as _dates

BRAND = " Nike.com"
TITLE = "Facture"

INVOICE_NO_LABEL = "Numéro de la Facture"
ORDER_NO_LABEL = "Numéro de la Commande"
INVOICE_DATE_LABEL = "Date de la Facture"
SHIP_DATE_LABEL = "Date d'Envoi"
DUE_DATE_LABEL = "Date D'échéance"

ORDER_LABEL = "Commande"
SHIPPED_TO_LABEL = "expédiée à"
INVOICE_LABEL = "Facture"
BILLED_TO_LABEL = "adressée à"

NOM = "Martin"
PRENOM = "Lucas"
CLIENT_NOM = "Martin Lucas"
ADRESSE = "12 Rue des Fleurs"
CP_VILLE = "75011 Paris"
PAYS = "FRANCE"

LIVRAISON_ADRESSE = "12 RUE DES FLEURS"
LIVRAISON_CP_VILLE = "75011 PARIS"
LIVRAISON_PAYS = "FRANCE"

NUM_FACTURE = "FR1024736093"
NUM_COMMANDE = "C01402544289"

SELLER = "NIKE Retail B.V.,65-67 avenue des Champs-Elysees, Paris, 75008, France"
VAT = "VAT Reg. No:FR81405395518"
NOTICE_1 = (
    "Important - Merci de ne pas utiliser cette adresse pour les retours. "
    "Si tu veux retourner ta commande, consulte la rubrique Aide dans la"
)
NOTICE_PREFIX = "section 'Retours ' "
NOTICE_LINK = "www.nike.com"
NOTICE_SUFFIX = " Link."
PAGE = "Page 1 of 1"

COL_SKU = "Numéro de produit"
COL_DESC = "Description"
COL_QTY = "Quantité"
COL_SHIPPED = "Expédiée"
COL_UNIT = "Prix Unitaire"
COL_GROSS = "Brut"
COL_DISC = "Remise"
COL_PRICE = "Prix"
COL_UNIT_2 = "Unitaire"
COL_NET = "Net"
COL_TOTAL = "Prix Total"
COL_VAT = "TVA %"

SKU = "FB7921"
DESC = (
    "Sweat à capuche et zip Nike\n"
    "Sportswear Tech Fleece Windrunner\n"
    "pour homme"
)
QTE = "1.00"
BRUT = "119,99"
REMISE = "60,00"
TVA = "20"

SKU_2 = "FB8002"
DESC_2 = (
    "Pantalon de jogging Nike Sportswear\n"
    "Tech Fleece pour homme"
)
QTE_2 = "1.00"
BRUT_2 = "99,99"
REMISE_2 = "50,00"
TVA_2 = "20"

SHIP_LABEL = "Envoi"
SHIP_QTE = "1"

TOTAL_HT = "Total Hors TVA:"
TOTAL_VAT = "TVA:"
TOTAL_TTC = "Montant Total de la Facture:"
PAY_LABEL = "Mode(s) de Paiement:"
PAY_MODE = "Carte de Crédit"


def slash_date(d=None) -> str:
    return _dates.nike_invoice(d)
