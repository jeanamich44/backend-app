from app.services.generate_docs.common import example_dates as _dates

TITLE = "Facture"

SERVICE_TITLE = "Service client de la boutique en ligne"
SERVICE_ROWS = (
    ("Téléphone ", ":  0805-111637"),
    ("Ouverture ", ":  Lun-Ven 9:00-/7,00; Sam, 10:00-17:00"),
    ("E-Mail        ", ":  service@onlineshop.adidas.fr      "),
    ("URL     ", ":  www.adidas.fr"),
    ("Aide", ":  www.adidas.fr/aide"),
)

BILL_TITLE = "Adresse de facturation"
SHIP_TITLE = "Adresse de livraison"

NOM = "Martin"
PRENOM = "Lucas"
CLIENT_NOM = "Martin Lucas"
ADRESSE = "12 Rue des Fleurs"
CP_VILLE = "75011 Paris"
PAYS = "FR"

ASK = "Pour toute demande, merci d'indiquer ton:"
REF_LABELS = (
    "N° de commande",
    "N° de facture",
    "Date de la facture",
    "Date de livraison",
)

NUM_COMMANDE = "AFR90132922"
NUM_FACTURE = "FRADIN0007203672"


def __getattr__(name: str):
    if name == "DATE_FACTURE":
        return _dates.adidas_invoice()
    if name == "DATE_LIVRAISON":
        return _dates.adidas_delivery()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

COL_ARTICLE = "Article n°"
COL_TAILLE = "Taille"
COL_NOM = "Nom de produit"
COL_QTE = "Qté"
COL_PU = "Prix unitaire"
COL_HT = "(HT)"
COL_TTC = "(TTC)"
COL_PRIX_TOTAL = "Prix total"
COL_EUR = "EUR"

SKU = "AD1001"
TAILLE = "42"
PRODUIT = "SUPERSTAR"
QTE = "1"
PU_HT = "291,67"
PU_TTC = "350,00"
TOTAL = "350,00"

SUBTOTAL = "Sous-total avant remise"
MONTANT = "Montant de la facture"
TVA_PREFIX = "TVA incluse taux de 20% (HT "
NOTE = (
    "Le montant correspondant à la facture a été",
    "débité de ton compte.",
)

LEGAL = (
    "adidas International Trading B.V. * Atlas Arena, Afrika Building * Hoogoorddreef 9a * 1101 BA Amsterdam ZO * Pays-Bas",
    "adidas International Trading B.V., a son siège a Amsterdam et est enregistrée auprès de la Chambre de Commerce d'Amsterdam sous le numéro",
    "33305842, TVA NL-807301322B01",
    "N°TVA: FR 8243.81.877.91",
)
