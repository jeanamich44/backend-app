from datetime import datetime

LOGO = "Cdiscount - Marketplace"
TITLE = "Preuve d'achat"
ORDER_L1 = "Informations détaillées relative à la"
ORDER_L2 = "commande N° "
DATE_PREFIX = "Date de commande "
CLIENT = "Informations Client"
BILL_TITLE = "Adresse de facturation"
SHIP_TITLE = "Adresse de livraison"

NOM = "Malatray"
PRENOM = "Antoine"
CLIENT_NOM = "Antoine Malatray"
ADRESSE = "2 RUE ALEXANDRE DUMAS"
CP_VILLE = "94800 VILLEJUIF"
CIVILITY = "M. "
NUM_COMMANDE = "2604070231S1C0X"

PRODUCT = "Informations relatives au produit"
PAY_LABEL = "Mode de réglement"
COL_PRODUIT = "Produit(s) commandé(s)"
COL_QTE = "Qté"
COL_MNT = "Montant de l\u2019article"
TOTAL = "Total"
PORT = "FRAIS DE PORT"
VENDOR = "Informations relatives au vendeur"
VENDOR_LINK = "Voir la boutique vendeur"
VENDOR_BY = "Vendu par "
VENDOR_IMMAT = "Numéro d\u2019immatriculation "

DESC = "APPLE iPhone 14 128GB"
QTE = "1"
MONTANT = "271,99"
PORT_AMT = "0,00"
PAYMENT = "Carte Bancaire"
VENDEUR_CDISCOUNT = "CDISCOUNT"
IMMAT_CDISCOUNT = "RCS BORDEAUX 424 059 822"
VENDEUR_MKP = "KXYTRADE"
IMMAT_MKP = "J2025074480006"
VENDEUR = "CDISCOUNT"
IMMAT = "RCS BORDEAUX 424 059 822"

NOTE = "Note importante : Ceci n\u2019est pas une facture"
CGU = "Conditions Générales d\u2019Utilisation de la Marketplace Cdiscount"
LEGAL = (
    "CDISCOUNT, Société anonyme, au capital de 87 122 439,88€,",
    "n°RCS : 424 059 822,",
    "120 - 126 quai de Bacalan 33000 Bordeaux",
)


def slash_date(d=None) -> str:
    d = d or datetime.now()
    return f"{d:%d/%m/%Y}"
