def get_form_schema() -> dict:
    return {
        "defaults": {
            "cp": "75011",
            "nom": "Martin",
            "pays": "FR",
            "items": [
                {
                    "nom": "SUPERSTAR",
                    "qte": "1",
                    "sku": "AD1001",
                    "pu_ht": "291,67",
                    "pu_ttc": "350,00",
                    "taille": "42"
                }
            ],
            "total": "350,00",
            "ville": "Paris",
            "prenom": "Lucas",
            "adresse": "12 Rue des Fleurs",
            "cp_ville": "75011 Paris",
            "num_facture": "FRADIN0007203672",
            "date_facture": "09.09.2026",
            "livraison_cp": "75011",
            "num_commande": "AFR90132922",
            "livraison_nom": "Martin",
            "date_livraison": "09.09.2026",
            "livraison_pays": "FR",
            "livraison_ville": "Paris",
            "livraison_prenom": "Lucas",
            "livraison_adresse": "12 Rue des Fleurs",
            "livraison_cp_ville": "75011 Paris"
        },
        "metadata": {
            "logo": "/logos/adidas.svg",
            "title": "GÉNÉRATEUR FACTURE ADIDAS",
            "apiBase": "/api/generate-docs/facture/adidas",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "headerBg": "bg-white border-white/20",
            "maxItems": 7,
            "priceKey": "adidas",
            "subtitle": "Document PDF Adidas officiel",
            "backLabel": "Retour aux factures",
            "itemLabel": "4. Articles",
            "generateLabel": "Générer la facture",
            "filenameTemplate": "Facture_Adidas.pdf"
        },
        "sections": [
            {
                "title": "1. Adresse de facturation",
                "fields": [
                    {
                        "key": "nom",
                        "kind": "text",
                        "span": 1,
                        "label": "Nom",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        }
                    },
                    {
                        "key": "prenom",
                        "kind": "text",
                        "span": 1,
                        "label": "Prénom",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        }
                    },
                    {
                        "key": "adresse",
                        "kind": "text",
                        "span": 2,
                        "label": "Adresse",
                        "rules": {
                            "max": 50,
                            "min": 4,
                            "required": True
                        },
                        "autocompleteType": "address"
                    },
                    {
                        "key": "cp",
                        "kind": "text",
                        "span": 1,
                        "label": "Code postal",
                        "rules": {
                            "max": 10,
                            "min": 4,
                            "required": True
                        },
                        "autocompleteType": "city"
                    },
                    {
                        "key": "ville",
                        "kind": "text",
                        "span": 1,
                        "label": "Ville",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        },
                        "autocompleteType": "city"
                    },
                    {
                        "key": "pays",
                        "kind": "country",
                        "span": 2,
                        "label": "Pays",
                        "rules": {
                            "max": 30,
                            "min": 2,
                            "required": True
                        },
                        "advanced": True,
                        "placeholder": "Sélectionner un pays"
                    }
                ]
            },
            {
                "title": "2. Adresse de livraison",
                "fields": [
                    {
                        "key": "livraison_nom",
                        "kind": "text",
                        "span": 1,
                        "label": "Nom",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        }
                    },
                    {
                        "key": "livraison_prenom",
                        "kind": "text",
                        "span": 1,
                        "label": "Prénom",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        }
                    },
                    {
                        "key": "livraison_adresse",
                        "kind": "text",
                        "span": 2,
                        "label": "Adresse",
                        "rules": {
                            "max": 50,
                            "min": 4,
                            "required": True
                        },
                        "autocompleteType": "address"
                    },
                    {
                        "key": "livraison_cp",
                        "kind": "text",
                        "span": 1,
                        "label": "Code postal",
                        "rules": {
                            "max": 10,
                            "min": 4,
                            "required": True
                        },
                        "autocompleteType": "city"
                    },
                    {
                        "key": "livraison_ville",
                        "kind": "text",
                        "span": 1,
                        "label": "Ville",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        },
                        "autocompleteType": "city"
                    },
                    {
                        "key": "livraison_pays",
                        "kind": "country",
                        "span": 2,
                        "label": "Pays de livraison",
                        "rules": {
                            "max": 30,
                            "min": 2,
                            "required": True
                        },
                        "advanced": True,
                        "placeholder": "Sélectionner un pays"
                    }
                ]
            },
            {
                "title": "3. Références",
                "fields": [
                    {
                        "key": "num_commande",
                        "kind": "text",
                        "span": 1,
                        "label": "N° de commande",
                        "rules": {
                            "max": 24,
                            "min": 3,
                            "required": True
                        },
                        "placeholder": "AFR90132922"
                    },
                    {
                        "key": "num_facture",
                        "kind": "text",
                        "span": 1,
                        "label": "N° de facture",
                        "rules": {
                            "max": 24,
                            "min": 3,
                            "required": True
                        },
                        "placeholder": "FRADIN0007203672"
                    },
                    {
                        "key": "date_facture",
                        "kind": "date",
                        "span": 1,
                        "label": "Date de la facture",
                        "rules": {
                            "required": True
                        },
                        "dateFormat": "dot"
                    },
                    {
                        "key": "date_livraison",
                        "kind": "date",
                        "span": 1,
                        "label": "Date de livraison",
                        "rules": {
                            "required": True
                        },
                        "dateFormat": "dot"
                    }
                ]
            },
            {
                "title": "5. Calculs & Montants",
                "fields": [
                    {
                        "key": "total",
                        "kind": "text",
                        "span": 2,
                        "label": "Total à payer TTC (€)",
                        "rules": {
                            "max": 14,
                            "min": 1,
                            "required": True
                        },
                        "placeholder": "350,00"
                    }
                ],
                "position": "after_items"
            }
        ],
        "itemBlank": {
            "nom": "",
            "qte": "1",
            "sku": "",
            "pu_ht": "0,00",
            "pu_ttc": "0,00",
            "taille": ""
        },
        "itemColumns": [
            {
                "key": "sku",
                "label": "Article n°"
            },
            {
                "key": "taille",
                "label": "Taille"
            },
            {
                "key": "nom",
                "label": "Nom de produit"
            },
            {
                "key": "qte",
                "label": "Qté"
            },
            {
                "key": "pu_ht",
                "label": "Prix unitaire HT"
            },
            {
                "key": "pu_ttc",
                "label": "Prix unitaire TTC"
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
                    "label": "Logo Adidas",
                    "master": False,
                    "section": "header"
                },
                {
                    "id": "header_title",
                    "label": "Titre Facture",
                    "master": False,
                    "section": "header"
                },
                {
                    "id": "header_service",
                    "label": "Service client / Coordonnées",
                    "master": False,
                    "section": "header"
                },
                {
                    "id": "header_addresses",
                    "label": "Adresses Facturation & Livraison",
                    "master": False,
                    "section": "header"
                },
                {
                    "id": "header_refs",
                    "label": "Références Commande & Dates",
                    "master": False,
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
                    "label": "En-tête colonnes tableau",
                    "master": False,
                    "section": "middle"
                },
                {
                    "id": "middle_rows",
                    "label": "Lignes d'articles",
                    "master": False,
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Sous-totaux, TVA & Total",
                    "master": False,
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_line",
                    "label": "Ligne de séparation",
                    "master": False,
                    "section": "footer"
                },
                {
                    "id": "footer_legal",
                    "label": "Mentions légales Adidas",
                    "master": False,
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "footer_line": True,
                "header_logo": True,
                "header_refs": True,
                "middle_rows": True,
                "footer_legal": True,
                "header_title": True,
                "middle_totals": True,
                "header_service": True,
                "middle_columns": True,
                "header_addresses": True
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
