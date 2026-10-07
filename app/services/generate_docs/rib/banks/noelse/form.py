from . import copy

def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR RIB NOELSE",
            "logo": "noelse",
            "apiBase": "/api/generate-docs/rib/noelse",
            "headerBg": "bg-gradient-to-br from-indigo-950/40 to-slate-950/80 border-indigo-500/30",
            "priceKey": "noelse",
            "subtitle": "Document PDF Noelse officiel",
            "filenameTemplate": f"RIB_Noelse_{copy.NOM}.pdf"
        },
        "defaults": {
            "nom": copy.NOM,
            "prenom": copy.PRENOM,
            "adresse": copy.ADRESSE,
            "cp": copy.CP,
            "ville": copy.VILLE,
            "pays": copy.PAYS,
            "code_banque": copy.BANQUE,
            "guichet": copy.GUICHET,
            "compte": copy.COMPTE,
            "cle": copy.CLE,
            "iban": copy.IBAN,
            "bic": copy.BIC,
            "header": "true",
            "header_logo": "true",
            "header_title": "true",
            "middle": "true",
            "middle_titulaire": "true",
            "middle_table": "true",
            "middle_iban": "true",
            "middle_bic": "true",
            "header_title_text": copy.TITLE
        },
        "sections": [
            {
                "id": "titulaire_section",
                "title": "Titulaire",
                "order": 1,
                "fields": [
                    {
                        "key": "nom",
                        "label": "Nom",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "EX: MARTIN",
                        "rules": {"required": True, "min": 2, "max": 35, "transform": "uppercase"}
                    },
                    {
                        "key": "prenom",
                        "label": "Prénom",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "EX: LUCAS",
                        "rules": {"required": True, "min": 2, "max": 35, "transform": "uppercase"}
                    },
                    {
                        "key": "adresse",
                        "label": "Adresse",
                        "kind": "address",
                        "span": 2,
                        "placeholder": "EX: 12 RUE DES FLEURS",
                        "rules": {"required": True, "min": 5, "max": 60}
                    },
                    {
                        "key": "cp",
                        "label": "Code postal",
                        "kind": "cp",
                        "span": 1,
                        "placeholder": "EX: 75011",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "ville",
                        "label": "Ville",
                        "kind": "ville",
                        "span": 1,
                        "placeholder": "EX: PARIS",
                        "rules": {"required": True, "min": 2, "max": 45}
                    },
                    {
                        "key": "pays",
                        "label": "Pays",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "France",
                        "rules": {"required": False, "min": 2, "max": 45}
                    }
                ]
            },
            {
                "id": "compte_section",
                "title": "Coordonnées bancaires",
                "order": 2,
                "fields": [
                    {
                        "key": "code_banque",
                        "label": "Code Banque",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "banque",
                        "placeholder": "16330",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "guichet",
                        "label": "Code Guichet",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "guichet",
                        "placeholder": "00001",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "compte",
                        "label": "N° de Compte",
                        "kind": "alnum",
                        "span": 1,
                        "autoIban": "compte",
                        "placeholder": "00012345678",
                        "rules": {"required": True, "min": 11, "max": 11, "transform": "uppercase"}
                    },
                    {
                        "key": "cle",
                        "label": "Clé RIB",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "cle",
                        "placeholder": "54",
                        "rules": {"required": True, "min": 2, "max": 2, "transform": "digits_only"}
                    },
                    {
                        "key": "iban",
                        "label": "IBAN",
                        "kind": "iban",
                        "span": 2,
                        "placeholder": "FR76 1633 0000 0100 0123 4567 854",
                        "rules": {"required": True, "min": 27, "max": 34, "transform": "uppercase"}
                    },
                    {
                        "key": "bic",
                        "label": "BIC / SWIFT",
                        "kind": "bic",
                        "span": 2,
                        "placeholder": "AFOPFR21XXX",
                        "rules": {"required": True, "min": 8, "max": 11, "transform": "uppercase"}
                    }
                ]
            },
            {
                "id": "header_section",
                "title": "En-tête",
                "order": 3,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "header_title_text",
                        "label": "Titre de l'en-tête",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "IBAN",
                        "rules": {"max": 40}
                    }
                ]
            }
        ],
        "customLayout": {
            "sections": [
                {"id": "header", "label": "En-tête"},
                {"id": "middle", "label": "Corps du document"}
            ],
            "blocks": [
                {"id": "header", "label": "En-tête", "master": True, "section": "header"},
                {"id": "header_logo", "label": "Logo", "master": False, "section": "header"},
                {"id": "header_title", "label": "Titre", "master": False, "section": "header"},
                {"id": "middle", "label": "Corps du document", "master": True, "section": "middle"},
                {"id": "middle_titulaire", "label": "Bloc titulaire", "master": False, "section": "middle"},
                {"id": "middle_table", "label": "Tableau RIB", "master": False, "section": "middle"},
                {"id": "middle_iban", "label": "IBAN", "master": False, "section": "middle"},
                {"id": "middle_bic", "label": "BIC", "master": False, "section": "middle"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_title": True,
                "middle": True,
                "middle_titulaire": True,
                "middle_table": True,
                "middle_iban": True,
                "middle_bic": True
            }
        }
    }
