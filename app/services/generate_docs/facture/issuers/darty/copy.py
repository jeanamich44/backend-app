from datetime import datetime

PAGE = "Page 1 / 1"
ISSUER = (
    "DARTY GRAND EST",
    "Service Comptabilité",
    "TSA n° 80 004",
    "93145 - Bondy cedex",
    "Téléphone : 01 48 02 34 35",
    "Télécopie : 01 48 02 77 80",
    "0 978 970 970 (prix d'un appel local)",
)
LABEL_SHIP = "Livraison"
LABEL_BILL = "Facturation"
TITLE = "JUSTIFICATIF DE VENTE (valant facture)"
UNDER = "_"
DATE_PREFIX = "Le "
ORDER_L = "Votre commande  "
ORDER_MID = "  du "
COL_REF = "Référence"
COL_QTE = "Qté"
COL_LIB = "Libellé"
COL_DATE = "Date"
COL_DELIV = "délivrance"
COL_HT = "Total HT"
COL_BASE = "Base / Taux"
COL_TVA = "TVA ou TCA"
COL_TTC = "Total TTC"
PIECES = "Disponibilité des pièces détachées : 5 ans"
ECO = "Dont éco-participation DEEE"
TRUST = "Le contrat de confiance."
TOTAL = "Total facturé : "
PAY = "Montant réglé par :  "
SOLDE = "Solde à régler :  "
LEGAL = (
    "DARTY GRAND EST - SNC au capital de 394 205 EUR - RCS LYON B 303 376 586 - code NAF 524 L",
    "Adresse : RN6 - BP38 - 69578 LIMONEST cedex",
    "TVA intracommunautaire : FR 13 303 376 586",
)

CIVILITY = "M. "
NOM = "Martin"
PRENOM = "Lucas"
CLIENT_NOM = "Martin Lucas"
ADRESSE = "12 RUE DES FLEURS"
CP_VILLE = "75011 PARIS"
PAYS = "France"
NUM_COMMANDE = "10011001"

SKU = "10011001"
DESC = "Casque bluetooth"
DESC2 = "Sans fil"
QTE = "1"
HT = "80,00"
TVA = "20,00"
PAYMENT = "PayPal"


def slash_date(d=None) -> str:
    d = d or datetime.now()
    return f"{d:%d/%m/%Y}"
