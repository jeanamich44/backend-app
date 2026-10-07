from . import copy

def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR RIB CRÉDIT MUTUEL",
            "logo": "cm",
            "apiBase": "/api/generate-docs/rib/cm",
            "headerBg": "bg-gradient-to-br from-rose-900/40 to-slate-950/80 border-rose-500/30",
            "priceKey": "cm",
            "subtitle": "Document PDF Crédit Mutuel officiel",
            "filenameTemplate": f"RIB_CM_{copy.NOM}.pdf"
        },
        "defaults": {
            "civilite": copy.CIVILITE,
            "nom": copy.NOM,
            "prenom": copy.PRENOM,
            "adresse": copy.ADRESSE,
            "cp": copy.CP,
            "ville": copy.VILLE,
            "agence_nom": copy.AGENCE,
            "agence_adresse": copy.DOMICILIATION_RUE,
            "agence_cp": copy.DOMICILIATION_CP,
            "agence_ville": copy.DOMICILIATION_VILLE,
            "agence_tel": copy.PHONE,
            "devise": copy.DEVISE,
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
            "middle_table": "true",
            "middle_agence": "true",
            "middle_iban": "true",
            "middle_bic": "true",
            "middle_domiciliation": "true",
            "middle_titulaire": "true",
            "middle_notice": "true",
            "middle_reserved": "true",
            "middle_lines": "true",
            "header_title_text": copy.TITLE,
            "middle_notice_text": copy.NOTICE
        },
        "sections": [
            {
                "id": "titulaire",
                "title": "Titulaire du compte",
                "order": 1,
                "fields": [
                    {
                        "key": "civilite",
                        "label": "Civilité",
                        "kind": "select",
                        "span": 1,
                        "options": [
                            {"label": "Monsieur (M.)", "value": "M."},
                            {"label": "Madame (MME)", "value": "MME"},
                            {"label": "Mademoiselle (MLLE)", "value": "MLLE"}
                        ],
                        "rules": {"required": True}
                    },
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
                        "rules": {"required": True, "min": 5, "max": 60, "transform": "uppercase"}
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
                        "rules": {"required": True, "min": 2, "max": 45, "transform": "uppercase"}
                    }
                ]
            },
            {
                "id": "agence",
                "title": "Agence",
                "order": 2,
                "fields": [
                    {
                        "key": "agence_nom",
                        "label": "Nom de l'agence",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "EX: CM PARIS CENTRE",
                        "rules": {"required": True, "min": 2, "max": 40, "transform": "uppercase"}
                    },
                    {
                        "key": "agence_adresse",
                        "label": "Adresse de l'agence",
                        "kind": "address",
                        "span": 2,
                        "placeholder": "EX: 15 RUE DE LA PAIX",
                        "rules": {"required": True, "min": 5, "max": 60, "transform": "uppercase"}
                    },
                    {
                        "key": "agence_cp",
                        "label": "Code postal agence",
                        "kind": "cp",
                        "span": 1,
                        "placeholder": "EX: 75002",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "agence_ville",
                        "label": "Ville agence",
                        "kind": "ville",
                        "span": 1,
                        "placeholder": "EX: PARIS",
                        "rules": {"required": True, "min": 2, "max": 45, "transform": "uppercase"}
                    },
                    {
                        "key": "agence_tel",
                        "label": "Téléphone agence",
                        "kind": "digits",
                        "span": 1,
                        "placeholder": "EX: 0100000000",
                        "rules": {"required": False, "min": 10, "max": 20, "transform": "digits_only"}
                    },
                    {
                        "key": "devise",
                        "label": "Devise",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "EUR",
                        "rules": {"required": True, "min": 1, "max": 5, "transform": "uppercase"}
                    }
                ]
            },
            {
                "id": "coordonnees_bancaires",
                "title": "Coordonnées Bancaires",
                "order": 3,
                "fields": [
                    {
                        "key": "code_banque",
                        "label": "Code Banque",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "banque",
                        "placeholder": "10278",
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
                        "placeholder": "41",
                        "rules": {"required": True, "min": 2, "max": 2, "transform": "digits_only"}
                    },
                    {
                        "key": "iban",
                        "label": "IBAN",
                        "kind": "iban",
                        "span": 2,
                        "placeholder": "FR76 1027 8000 0100 0123 4567 841",
                        "rules": {"required": True, "min": 27, "max": 34, "transform": "uppercase"}
                    },
                    {
                        "key": "bic",
                        "label": "BIC / SWIFT",
                        "kind": "bic",
                        "span": 2,
                        "placeholder": "CMCIFRPP",
                        "rules": {"required": True, "min": 8, "max": 11, "transform": "uppercase"}
                    }
                ]
            },
            {
                "id": "header_section",
                "title": "En-tête",
                "order": 4,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "header_title_text",
                        "label": "Titre de l'en-tête",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "RELEVE D’IDENTITE BANCAIRE",
                        "rules": {"max": 40}
                    }
                ]
            },
            {
                "id": "middle_section",
                "title": "Corps",
                "order": 5,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "middle_notice_text",
                        "label": "Notice explicative",
                        "kind": "textarea",
                        "span": 2,
                        "placeholder": "Remettez ce relevé à tout autre organisme...",
                        "rules": {"max": 400}
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
                {"id": "middle_table", "label": "Tableau RIB", "master": False, "section": "middle"},
                {"id": "middle_agence", "label": "Bloc agence", "master": False, "section": "middle"},
                {"id": "middle_iban", "label": "IBAN", "master": False, "section": "middle"},
                {"id": "middle_bic", "label": "BIC", "master": False, "section": "middle"},
                {"id": "middle_domiciliation", "label": "Bloc domiciliation", "master": False, "section": "middle"},
                {"id": "middle_titulaire", "label": "Bloc titulaire", "master": False, "section": "middle"},
                {"id": "middle_notice", "label": "Notice", "master": False, "section": "middle"},
                {"id": "middle_reserved", "label": "Partie réservée", "master": False, "section": "middle"},
                {"id": "middle_lines", "label": "Filets / lignes", "master": False, "section": "middle"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_title": True,
                "middle": True,
                "middle_table": True,
                "middle_agence": True,
                "middle_iban": True,
                "middle_bic": True,
                "middle_domiciliation": True,
                "middle_titulaire": True,
                "middle_notice": True,
                "middle_reserved": True,
                "middle_lines": True
            }
        }
    }
