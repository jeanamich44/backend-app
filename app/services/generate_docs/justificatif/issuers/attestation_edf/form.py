from . import copy

# ----------------------------------------------------------------------


def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR ATTESTATION EDF",
            "subtitle": "Attestation titulaire de contrat",
            "logo": "/logos/edf.svg",
            "headerBg": "bg-white border-orange-500/30",
            "priceKey": "attestation_edf",
            "apiBase": "/api/generate-docs/justificatif/attestation_edf",
            "filenameTemplate": "Attestation_EDF.pdf",
            "generateLabel": "Générer le justificatif",
            "backHref": "/services/generate-docs/justificatif",
            "backLabel": "Retour aux justificatifs"
        },
        "defaults": {
            "civilite": copy.CIVILITE,
            "nom": copy.NOM,
            "prenom": copy.PRENOM,
            "adresse": copy.ADRESSE,
            "cp": copy.CP,
            "ville": copy.VILLE,
            "num_client": copy.NUM_CLIENT,
            "num_compte": copy.NUM_COMPTE,
            "pdl": copy.PDL,
            "puissance": copy.PUISSANCE,
            "date": copy.DATE,
            "email": copy.EMAIL,
            "conseillere": copy.CONSEILLERE,
            "footer_cachet": copy.FOOTER_CACHET
        },
        "sections": [
            {
                "id": "titulaire",
                "title": "1. Titulaire",
                "order": 1,
                "fields": [
                    {
                        "key": "civilite",
                        "label": "Civilité",
                        "kind": "select",
                        "span": 1,
                        "rules": {"required": False},
                        "options": [
                            {"label": "Mr.", "value": "Mr."},
                            {"label": "Mme.", "value": "Mme."},
                            {"label": "Mlle.", "value": "Mlle."},
                            {"label": "Rien", "value": "__NONE__"},
                            {"label": "Personnalisé", "value": "__CUSTOM__"}
                        ]
                    },
                    {
                        "key": "nom",
                        "label": "Nom",
                        "kind": "text",
                        "span": 1,
                        "rules": {"min": 2, "max": 40, "required": True, "transform": "uppercase"},
                        "required": True,
                        "min": 2,
                        "max": 40,
                        "placeholder": "ex: Martin"
                    },
                    {
                        "key": "prenom",
                        "label": "Prénom",
                        "kind": "text",
                        "span": 1,
                        "rules": {"min": 2, "max": 40, "required": True, "transform": "uppercase"},
                        "required": True,
                        "min": 2,
                        "max": 40,
                        "placeholder": "ex: Lucas"
                    },
                    {
                        "key": "adresse",
                        "label": "Adresse",
                        "kind": "text",
                        "span": 2,
                        "rules": {"min": 5, "max": 80, "required": True},
                        "required": True,
                        "min": 5,
                        "max": 80,
                        "placeholder": "ex: 12 Rue des Fleurs",
                        "autocompleteType": "address"
                    },
                    {
                        "key": "cp",
                        "label": "Code postal",
                        "kind": "text",
                        "span": 1,
                        "rules": {"min": 5, "max": 5, "required": True},
                        "required": True,
                        "min": 5,
                        "max": 5,
                        "placeholder": "ex: 75011"
                    },
                    {
                        "key": "ville",
                        "label": "Ville",
                        "kind": "text",
                        "span": 1,
                        "rules": {"min": 2, "max": 50, "required": True, "transform": "uppercase"},
                        "required": True,
                        "min": 2,
                        "max": 50,
                        "placeholder": "ex: Paris"
                    }
                ]
            },
            {
                "id": "contrat",
                "title": "2. Contrat",
                "order": 2,
                "fields": [
                    {
                        "key": "num_client",
                        "label": "N° client",
                        "kind": "text",
                        "span": 1,
                        "rules": {"min": 10, "max": 14, "required": True},
                        "required": True,
                        "min": 10,
                        "max": 14,
                        "placeholder": "ex: 6 013 159 667"
                    },
                    {
                        "key": "num_compte",
                        "label": "N° de compte",
                        "kind": "text",
                        "span": 1,
                        "rules": {"min": 13, "max": 20, "required": True},
                        "required": True,
                        "min": 13,
                        "max": 20,
                        "placeholder": "ex: 4 02 4 024 8 51 258"
                    },
                    {
                        "key": "pdl",
                        "label": "PDL",
                        "kind": "text",
                        "span": 1,
                        "rules": {"min": 14, "max": 14, "required": True},
                        "required": True,
                        "min": 14,
                        "max": 14,
                        "placeholder": "ex: 07334145884965"
                    },
                    {
                        "key": "puissance",
                        "label": "Puissance (kVA)",
                        "kind": "text",
                        "span": 1,
                        "rules": {"min": 1, "max": 4, "required": True},
                        "required": True,
                        "min": 1,
                        "max": 4,
                        "placeholder": "ex: 06"
                    },
                    {
                        "key": "date",
                        "label": "Date",
                        "kind": "date",
                        "span": 2,
                        "dateFormat": "french",
                        "rules": {"required": True},
                        "required": True,
                        "placeholder": "ex: 8 Septembre 2026"
                    }
                ]
            },
            {
                "id": "contact",
                "title": "3. Contact",
                "order": 3,
                "fields": [
                    {
                        "key": "email",
                        "label": "Email service client",
                        "kind": "text",
                        "span": 1,
                        "rules": {"min": 5, "max": 80, "required": True},
                        "required": True,
                        "min": 5,
                        "max": 80,
                        "placeholder": "ex: serviceclient@edf.fr"
                    },
                    {
                        "key": "conseillere",
                        "label": "Conseillère",
                        "kind": "text",
                        "span": 1,
                        "rules": {"min": 2, "max": 40, "required": True},
                        "required": True,
                        "min": 2,
                        "max": 40,
                        "placeholder": "ex: Marie"
                    }
                ]
            },
            {
                "id": "cachet",
                "title": "4. Cachet 2D-DOC",
                "order": 4,
                "fields": [
                    {
                        "key": "footer_cachet",
                        "label": "Afficher le cachet 2D-DOC",
                        "kind": "checkbox",
                        "span": 2
                    }
                ]
            }
        ],
        "customLayout": {
            "blocks": [
                {"id": "header", "label": "En-tête complet", "master": True, "section": "header"},
                {"id": "header_logo", "label": "Logo EDF", "master": False, "section": "header"},
                {"id": "header_window", "label": "Fenêtre adresse titulaire", "master": False, "section": "header"},
                {"id": "header_title", "label": "Titre & objet de l'attestation", "master": False, "section": "header"},
                {"id": "header_contact", "label": "Bloc contact & coordonnées EDF", "master": False, "section": "header"},
                {"id": "middle", "label": "Corps complet de l'attestation", "master": True, "section": "middle"},
                {"id": "middle_body", "label": "Texte d'attestation de contrat", "master": False, "section": "middle"},
                {"id": "middle_lieu", "label": "Lieu de consommation, PDL & Puissance", "master": False, "section": "middle"},
                {"id": "middle_date", "label": "Date, conseillère & signature", "master": False, "section": "middle"},
                {"id": "footer", "label": "Pied de page", "master": True, "section": "footer"},
                {"id": "footer_legal", "label": "Mentions légales EDF SA", "master": False, "section": "footer"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_window": True,
                "header_title": True,
                "header_contact": True,
                "middle": True,
                "middle_body": True,
                "middle_lieu": True,
                "middle_date": True,
                "footer": True,
                "footer_legal": True
            },
            "sections": [
                {"id": "header", "label": "En-tête"},
                {"id": "middle", "label": "Corps de l'attestation"},
                {"id": "footer", "label": "Pied de page"}
            ]
        }
    }
