def get_form_schema() -> dict:
    return {
        "version": 6,
        "defaults": {
            "store_name": "PRINTEMPS PARLY 2",
            "store_code": "5921489590020",
            "facture_num": "8259",
            "num_facture": "8259",
            "date_facture": "02/09/2023",
            "ville_emission": "Neuilly Sur Marne",
            "mode_paiement": "Carte Bleue (Eu)",
            "payment_label": "Carte Bleue (Eu)",
            "total_ttc": "3 250.00",
            "items": [
                {
                    "code": "0B0006-6B0275",
                    "ref": "0B0006-6B0275",
                    "desc": "BRACELET FORCE 10 GRAND MODÈLE OR JAUNE\nAJUSTABLE\nFRED PARIS\nRéférence: 6B0146\nGravure: 1012846",
                    "designation": "BRACELET FORCE 10 GRAND MODÈLE OR JAUNE\nAJUSTABLE\nFRED PARIS\nRéférence: 6B0146\nGravure: 1012846",
                    "qty": "1",
                    "quantite": "1",
                    "prix_ttc": "3 250.00",
                    "unit_price": "3 250.00",
                    "total": "3 250.00"
                }
            ]
        },
        "metadata": {
            "logo": "/logos/fred.svg",
            "title": "Fred",
            "apiBase": "/api/generate-docs/facture/fred",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "headerBg": "bg-white border-neutral-800/30",
            "maxItems": 3,
            "priceKey": "fred",
            "subtitle": "Facture boutique Fred Joaillerie",
            "backLabel": "Retour aux factures",
            "itemLabel": "Articles",
            "logoClass": "scale-100 md:scale-105",
            "generateLabel": "Générer la facture Fred",
            "filenameTemplate": "Facture_Fred.pdf"
        },
        "sections": [
            {
                "title": "1. Vente en boutique",
                "fields": [
                    {
                        "key": "store_name",
                        "kind": "text",
                        "span": 1,
                        "label": "Boutique / Point de vente",
                        "rules": {
                            "max": 50,
                            "required": True
                        },
                        "placeholder": "PRINTEMPS PARLY 2"
                    },
                    {
                        "key": "store_code",
                        "kind": "text",
                        "span": 1,
                        "label": "Code boutique / Siret",
                        "rules": {
                            "max": 30,
                            "required": False
                        },
                        "placeholder": "5921489590020"
                    },
                    {
                        "key": "facture_num",
                        "kind": "text",
                        "span": 1,
                        "label": "N° de facture",
                        "rules": {
                            "max": 20,
                            "min": 2,
                            "required": True
                        },
                        "placeholder": "8259"
                    },
                    {
                        "key": "date_facture",
                        "kind": "date",
                        "span": 1,
                        "label": "Date de la facture",
                        "rules": {
                            "required": True
                        },
                        "dateFormat": "slash",
                        "placeholder": "02/09/2023"
                    },
                    {
                        "key": "ville_emission",
                        "kind": "text",
                        "span": 1,
                        "label": "Lieu d'émission",
                        "rules": {
                            "max": 50,
                            "required": True
                        },
                        "placeholder": "Neuilly Sur Marne",
                        "autocompleteType": "city"
                    },
                    {
                        "key": "mode_paiement",
                        "kind": "select",
                        "span": 1,
                        "label": "Mode de règlement",
                        "rules": {
                            "max": 30,
                            "required": True
                        },
                        "options": [
                            {
                                "label": "Carte Bleue (Eu)",
                                "value": "Carte Bleue (Eu)"
                            },
                            {
                                "label": "Carte Bancaire",
                                "value": "CARTE BANCAIRE"
                            },
                            {
                                "label": "Espèces Euros",
                                "value": "ESPECES EUROS"
                            },
                            {
                                "label": "Visa",
                                "value": "VISA"
                            },
                            {
                                "label": "Mastercard",
                                "value": "MASTERCARD"
                            }
                        ]
                    }
                ]
            },
            {
                "title": "2. Totaux & Taxes",
                "position": "after_items",
                "fields": [
                    {
                        "key": "total_ttc",
                        "kind": "text",
                        "span": 1,
                        "label": "Total TTC (€)",
                        "rules": {
                            "max": 30,
                            "required": False
                        },
                        "placeholder": "3 250.00"
                    }
                ]
            }
        ],
        "itemBlank": {
            "qty": "1",
            "ref": "",
            "code": "",
            "desc": "",
            "total": "0,00",
            "quantite": "1",
            "unit_price": "0,00",
            "designation": ""
        },
        "itemColumns": [
            {
                "key": "code",
                "label": "Code article",
                "rules": {
                    "max": 30
                }
            },
            {
                "key": "desc",
                "label": "Désignation",
                "rules": {
                    "max": 120
                }
            },
            {
                "key": "qty",
                "label": "Qté",
                "rules": {
                    "max": 10
                }
            },
            {
                "key": "unit_price",
                "label": "Prix TTC (€)",
                "rules": {
                    "max": 20
                }
            }
        ],
        "itemsConfig": {
            "key": "items",
            "label": "Articles (3 maximum)",
            "columns": [
                {
                    "key": "code",
                    "kind": "text",
                    "label": "Code article",
                    "required": True
                },
                {
                    "key": "desc",
                    "kind": "text",
                    "label": "Désignation",
                    "required": True
                },
                {
                    "key": "qty",
                    "kind": "text",
                    "label": "Qté",
                    "required": True
                },
                {
                    "key": "unit_price",
                    "kind": "text",
                    "label": "Prix TTC (€)",
                    "required": True
                }
            ],
            "enabled": True,
            "maxItems": 3,
            "blankItem": {
                "qty": "1",
                "ref": "",
                "code": "",
                "desc": "",
                "total": "0,00",
                "quantite": "1",
                "unit_price": "0,00",
                "designation": ""
            }
        },
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
                    "label": "Logo boutique Fred",
                    "section": "header"
                },
                {
                    "id": "header_boutique",
                    "label": "Boutique et Siret",
                    "section": "header"
                },
                {
                    "id": "header_meta",
                    "label": "Date, lieu et n° facture",
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_table",
                    "label": "Tableau d'orfèvrerie & articles",
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Totaux & mode de paiement",
                    "section": "middle"
                }
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_boutique": True,
                "header_meta": True,
                "middle": True,
                "middle_table": True,
                "middle_totals": True
            },
            "sections": [
                {
                    "id": "header",
                    "label": "En-tête"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture"
                }
            ]
        }
    }
