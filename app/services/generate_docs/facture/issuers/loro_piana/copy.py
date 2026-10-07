"""Chrome boutique Loro Piana + dummy ticket (pas le PII gabarit)."""

from datetime import datetime

STORE = (
    "12 Rue du Faubourg Saint-Honoré, 75008 Paris",
    "Tel. 0033 04 04170705 Fax. 00377 97977537",
    "paris@loropiana.com www.loropiana.com",
)

TITLE = "Reçu"
LABEL_TICKET = "Numéro de ticket:"
LABEL_CAISSE = "Ticket de caisse:"
LABEL_DATE = "Date:"
LABEL_CASHIER = "Caissier:"

NUM_TICKET = "291"
TICKET_CAISSE = "FR75 - 13 - 7687"
NOM = "Martin"
PRENOM = "Lucas"
CAISSIER = "000097"

COL_ARTICLE = "Article"
COL_DESC = "Description"
COL_QTE = "Quantité"
COL_PRIX = "Prix"
COL_TOTAL = "Total"
TOTAL_N = "Total: "
TOTAL_FINAL = "Total final:"
TVA = "TVA:"
PAIEMENT = "Paiement:"
MONNAIE = "Monnaie rendue"

SKU = "JWWJ156916"
DESC = "SUMMER, WALK LOADERS, FAE8124"
QTE = "1"
PRIX = "820.00"
PAYMENT = "VISA"
MONNAIE_AMT = "0.00"
TVA_RATE = "20.00"


def ticket_datetime(d=None) -> str:
    d = d or datetime.now()
    return f"{d:%d-%m-%Y %H:%M:%S}"
