from . import copy

# ----------------------------------------------------------------------


def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR ATTESTATION DIRECT ÉNERGIE",
            "subtitle": "Attestation d'abonnement Direct énergie officielle",
            "logo": "/logos/direct_energie.svg",
            "headerBg": "bg-white border-amber-500/30",
            "priceKey": "attestation_direct_energie",
            "apiBase": "/api/generate-docs/justificatif/attestation_direct_energie",
            "filenameTemplate": "Attestation_Direct_Energie.pdf",
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
            "depuis": copy.DEPUIS,
            "date": copy.DATE
        },
        "sections": [
            {
                "id": "titulaire",
                "title": "1. Titulaire du contrat",
                "order": 1,
                "fields": [
                    {
                        "key": "civilite",
                        "label": "Civilité",
                        "kind": "select",
                        "span": 1,
                        "rules": {"required": False},
                        "options": [
                            {"label": "M.", "value": "M."},
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
                        "rules": {"min": 2, "max": 40, "required": True},
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
                        "rules": {"min": 2, "max": 40, "required": True},
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
                        "rules": {"min": 2, "max": 50, "required": True},
                        "required": True,
                        "min": 2,
                        "max": 50,
                        "placeholder": "ex: Paris"
                    }
                ]
            },
            {
                "id": "abonnement",
                "title": "2. Références d'abonnement",
                "order": 2,
                "fields": [
                    {
                        "key": "num_client",
                        "label": "Référence client",
                        "kind": "text",
                        "span": 1,
                        "rules": {"min": 5, "max": 20, "required": True},
                        "required": True,
                        "min": 5,
                        "max": 20,
                        "placeholder": "ex: 103866054"
                    },
                    {
                        "key": "depuis",
                        "label": "Client depuis le",
                        "kind": "date",
                        "span": 1,
                        "dateFormat": "french",
                        "rules": {"required": True},
                        "required": True,
                        "placeholder": "ex: 1 Janvier 2020"
                    },
                    {
                        "key": "date",
                        "label": "Fait à Paris, le",
                        "kind": "date",
                        "span": 2,
                        "dateFormat": "french",
                        "rules": {"required": True},
                        "required": True,
                        "placeholder": "ex: 8 Septembre 2026"
                    }
                ]
            }
        ],
        "customLayout": {
            "blocks": [
                {"id": "header", "label": "En-tête complet", "master": True, "section": "header"},
                {"id": "header_logo", "label": "Logo Direct Énergie", "section": "header"},
                {"id": "header_window", "label": "Bloc destinataire (fenêtre)", "section": "header"},
                {"id": "header_title", "label": "Titre du document & date", "section": "header"},
                {"id": "middle", "label": "Corps complet", "master": True, "section": "middle"},
                {"id": "middle_refs", "label": "Référence client", "section": "middle"},
                {"id": "middle_body", "label": "Texte de l'attestation", "section": "middle"},
                {"id": "middle_sign", "label": "Signature & Direction", "section": "middle"},
                {"id": "middle_note", "label": "Note justificatif de domicile", "section": "middle"},
                {"id": "footer", "label": "Pied de page complet", "master": True, "section": "footer"},
                {"id": "footer_site", "label": "Site web (jaune)", "section": "footer"},
                {"id": "footer_legal", "label": "Mentions légales", "section": "footer"},
                {"id": "footer_ref", "label": "Référence courrier", "section": "footer"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_window": True,
                "header_title": True,
                "middle": True,
                "middle_refs": True,
                "middle_body": True,
                "middle_sign": True,
                "middle_note": True,
                "footer": True,
                "footer_site": True,
                "footer_legal": True,
                "footer_ref": True
            },
            "sections": [
                {"id": "header", "label": "En-tête"},
                {"id": "middle", "label": "Corps du document"},
                {"id": "footer", "label": "Pied de page"}
            ]
        }
    }
