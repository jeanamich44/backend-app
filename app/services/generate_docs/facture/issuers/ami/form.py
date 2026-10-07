def get_form_schema() -> dict:
    return {
        "defaults": {
            "cp": "75011",
            "tva": "20",
            "items": [
                {
                    "pu": "80,00",
                    "qte": "1",
                    "desc": "Sweat capuche noir"
                }
            ],
            "ville": "Paris",
            "adresse": "12 Rue des Fleurs",
            "num_facture": "67 459",
            "total": "96,00"
        },
        "metadata": {
            "logo": "/logos/ami.png",
            "title": "GÉNÉRATEUR FACTURE AMI",
            "apiBase": "/api/generate-docs/facture/ami",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "category": "facture",
            "headerBg": "bg-white border-white/20",
            "maxItems": 2,
            "priceKey": "ami",
            "subtitle": "Document PDF AMI Paris officiel",
            "backLabel": "Retour aux factures",
            "itemLabel": "3. Articles",
            "generateLabel": "Générer la facture",
            "filenameTemplate": "Facture_AMI.pdf"
        },
        "sections": [
            {
                "title": "1. Client",
                "fields": [
                    {
                        "key": "adresse",
                        "label": "Adresse"
                    },
                    {
                        "key": "cp",
                        "label": "Code postal"
                    },
                    {
                        "key": "ville",
                        "label": "Ville"
                    }
                ]
            },
            {
                "title": "2. Références",
                "fields": [
                    {
                        "key": "num_facture",
                        "label": "N° de facture"
                    },
                    {
                        "key": "date_facture",
                        "kind": "date",
                        "label": "Date de la facture",
                        "dateFormat": "slash"
                    }
                ]
            },
            {
                "title": "3. Totaux",
                "position": "after_items",
                "fields": [
                    {
                        "key": "total",
                        "label": "Total TTC",
                        "placeholder": "96,00"
                    },
                    {
                        "key": "tva",
                        "label": "TVA %",
                        "advanced": True
                    }
                ]
            }
        ],
        "itemBlank": {
            "pu": "0,00",
            "qte": "1",
            "desc": ""
        },
        "itemColumns": [
            {
                "key": "desc",
                "label": "Description"
            },
            {
                "key": "qte",
                "label": "Quantité"
            },
            {
                "key": "pu",
                "label": "Prix unitaire HT"
            }
        ],
        "customLayout": {
            "blocks": [
                {
                    "id": "header",
                    "label": "En-tête complet",
                    "master": True,
                    "section": "header"
                },
                {
                    "id": "header_logo",
                    "label": "Logo AMI Paris",
                    "section": "header"
                },
                {
                    "id": "header_brand",
                    "label": "Marque & Titre",
                    "section": "header"
                },
                {
                    "id": "header_title",
                    "label": "Titre FACTURE",
                    "section": "header"
                },
                {
                    "id": "header_issuer",
                    "label": "Coordonnées émetteur (Mattiussi)",
                    "section": "header"
                },
                {
                    "id": "header_refs",
                    "label": "Références & Adresse client",
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_columns",
                    "label": "En-tête des colonnes",
                    "section": "middle"
                },
                {
                    "id": "middle_rows",
                    "label": "Lignes d'articles",
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Totaux & TVA",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_thanks",
                    "label": "Texte de remerciements",
                    "section": "footer"
                },
                {
                    "id": "footer_sign",
                    "label": "Signature & Formule",
                    "section": "footer"
                },
                {
                    "id": "footer_line",
                    "label": "Filet inférieur de séparation",
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "footer_line": True,
                "footer_sign": True,
                "header_logo": True,
                "header_refs": True,
                "middle_rows": True,
                "header_brand": True,
                "header_title": True,
                "footer_thanks": True,
                "header_issuer": True,
                "middle_totals": True,
                "middle_columns": True
            },
            "sections": [
                {
                    "id": "header",
                    "label": "En-tête"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture"
                },
                {
                    "id": "footer",
                    "label": "Pied de page"
                }
            ]
        }
    }
