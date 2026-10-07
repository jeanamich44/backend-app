from . import copy

def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR CERTIFICAT IBAN MYPOS",
            "logo": "mypos",
            "apiBase": "/api/generate-docs/rib/mypos",
            "headerBg": "bg-gradient-to-br from-blue-950/40 to-slate-950/80 border-blue-500/30",
            "priceKey": "mypos",
            "subtitle": "Document PDF myPOS officiel",
            "filenameTemplate": f"Certificat_IBAN_myPOS_{copy.TITULAIRE}.pdf"
        },
        "defaults": {
            "date_edition": copy.DATE,
            "nom_societe": copy.NOM_SOCIETE,
            "titulaire": copy.TITULAIRE,
            "num_enregistrement": copy.NUM_ENREGISTREMENT,
            "adresse": copy.ADRESSE,
            "cp": copy.CP,
            "ville": copy.VILLE,
            "pays": copy.PAYS,
            "num_compte_mypos": copy.COMPTE,
            "devise": copy.DEVISE,
            "iban": copy.IBAN,
            "bic": copy.BIC,
            "header": "true",
            "header_logo": "true",
            "header_title": "true",
            "header_date": "true",
            "header_address": "true",
            "middle": "true",
            "middle_letter": "true",
            "middle_table": "true",
            "footer": "true",
            "footer_legal": "true",
            "footer_page": "true",
            "header_title_text": copy.TITLE,
            "footer_page_text": copy.PAGE_NO
        },
        "sections": [
            {
                "id": "titulaire_section",
                "title": "Informations de l'entreprise",
                "order": 1,
                "fields": [
                    {
                        "key": "date_edition",
                        "label": "Date d'édition",
                        "kind": "date",
                        "span": 2,
                        "placeholder": "Septembre 07 2026",
                        "rules": {"required": False, "max": 25}
                    },
                    {
                        "key": "nom_societe",
                        "label": "Nom de la société",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "LUCAS ENTREPRISE SASU",
                        "rules": {"required": True, "min": 2, "max": 40}
                    },
                    {
                        "key": "titulaire",
                        "label": "Représenté par",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "MARTIN LUCAS",
                        "rules": {"required": True, "min": 2, "max": 40, "transform": "uppercase"}
                    },
                    {
                        "key": "num_enregistrement",
                        "label": "N° d'enregistrement / SIREN",
                        "kind": "digits",
                        "span": 1,
                        "placeholder": "123456789",
                        "rules": {"required": True, "min": 5, "max": 20, "transform": "digits_only"}
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
                    },
                    {
                        "key": "pays",
                        "label": "Pays",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "France Métropolitaine",
                        "rules": {"required": False, "min": 2, "max": 45}
                    }
                ]
            },
            {
                "id": "compte_section",
                "title": "Détails du compte",
                "order": 2,
                "fields": [
                    {
                        "key": "num_compte_mypos",
                        "label": "Numéro de compte myPOS",
                        "kind": "digits",
                        "span": 1,
                        "placeholder": "00012345",
                        "rules": {"required": True, "min": 4, "max": 20, "transform": "digits_only"}
                    },
                    {
                        "key": "devise",
                        "label": "Devise",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "EUR",
                        "rules": {"required": True, "min": 1, "max": 5, "transform": "uppercase"}
                    },
                    {
                        "key": "iban",
                        "label": "IBAN",
                        "kind": "iban",
                        "span": 2,
                        "placeholder": "IE12MPOS99039000012345",
                        "rules": {"required": True, "min": 15, "max": 34, "transform": "uppercase"}
                    },
                    {
                        "key": "bic",
                        "label": "BIC / SWIFT",
                        "kind": "bic",
                        "span": 2,
                        "placeholder": "MPOSIE2D",
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
                        "placeholder": "Certificat IBAN",
                        "rules": {"max": 40}
                    }
                ]
            },
            {
                "id": "footer_section",
                "title": "Pied de page",
                "order": 4,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "footer_page_text",
                        "label": "Numéro de page",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "1",
                        "rules": {"max": 10}
                    }
                ]
            }
        ],
        "customLayout": {
            "sections": [
                {"id": "header", "label": "En-tête"},
                {"id": "middle", "label": "Corps du document"},
                {"id": "footer", "label": "Pied de page"}
            ],
            "blocks": [
                {"id": "header", "label": "En-tête", "master": True, "section": "header"},
                {"id": "header_logo", "label": "Logo", "master": False, "section": "header"},
                {"id": "header_title", "label": "Titre", "master": False, "section": "header"},
                {"id": "header_date", "label": "Date document", "master": False, "section": "header"},
                {"id": "header_address", "label": "Adresse émetteur", "master": False, "section": "header"},
                {"id": "middle", "label": "Corps du document", "master": True, "section": "middle"},
                {"id": "middle_letter", "label": "Corps de la lettre", "master": False, "section": "middle"},
                {"id": "middle_table", "label": "Tableau récapitulatif", "master": False, "section": "middle"},
                {"id": "footer", "label": "Pied de page", "master": True, "section": "footer"},
                {"id": "footer_legal", "label": "Mentions légales", "master": False, "section": "footer"},
                {"id": "footer_page", "label": "Numéro de page", "master": False, "section": "footer"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_title": True,
                "header_date": True,
                "header_address": True,
                "middle": True,
                "middle_letter": True,
                "middle_table": True,
                "footer": True,
                "footer_legal": True,
                "footer_page": True
            }
        }
    }
