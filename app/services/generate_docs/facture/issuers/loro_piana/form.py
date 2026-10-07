def get_form_schema() -> dict:
    return {
        "version": 3,
        "defaults": {
            "items": [
                {
                    "sku": "JWWJ156916",
                    "desc": "SUMMER, WALK LOADERS, FAE8124",
                    "qte": "1",
                    "prix": "820,00"
                }
            ],
            "monnaie": "0,00",
            "payment": "VISA",
            "caissier": "000097",
            "tva_rate": "20,00",
            "num_ticket": "291",
            "ticket_caisse": "FR75 13 7687",
            "date_ticket": "05/08/2023",
            "heure_ticket": "19:10:13",
            "total": "820,00"
        },
        "metadata": {
            "logo": "/logos/loro_piana.png",
            "title": "GÉNÉRATEUR TICKET LORO PIANA",
            "apiBase": "/api/generate-docs/facture/loro_piana",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "headerBg": "bg-white border-neutral-800/30",
            "maxItems": 6,
            "priceKey": "loro_piana",
            "subtitle": "Ticket de caisse boutique Loro Piana officiel",
            "backLabel": "Retour aux factures",
            "itemLabel": "3. Articles",
            "logoClass": "scale-115 md:scale-125",
            "generateLabel": "Générer le ticket",
            "filenameTemplate": "Facture_Loro_Piana.pdf"
        },
        "sections": [
            {
                "title": "1. Caisse et Ticket",
                "fields": [
                    {
                        "key": "num_ticket",
                        "kind": "text",
                        "span": 1,
                        "label": "N° ticket",
                        "placeholder": "291",
                        "rules": {
                            "max": 12,
                            "required": True
                        }
                    },
                    {
                        "key": "ticket_caisse",
                        "kind": "text",
                        "span": 1,
                        "label": "Ticket de caisse",
                        "placeholder": "FR75 13 7687",
                        "rules": {
                            "max": 24,
                            "required": True
                        }
                    },
                    {
                        "key": "date_ticket",
                        "kind": "date",
                        "span": 1,
                        "label": "Date du ticket",
                        "placeholder": "05/08/2023",
                        "rules": {
                            "required": True
                        }
                    },
                    {
                        "key": "heure_ticket",
                        "kind": "time",
                        "span": 1,
                        "label": "Heure du ticket",
                        "placeholder": "19:10:13",
                        "rules": {
                            "required": True
                        }
                    },
                    {
                        "key": "caissier",
                        "kind": "text",
                        "span": 1,
                        "label": "Caissier",
                        "placeholder": "000097",
                        "rules": {
                            "max": 25,
                            "required": True
                        }
                    }
                ]
            },
            {
                "title": "2. Règlement",
                "fields": [
                    {
                        "key": "payment",
                        "kind": "select",
                        "span": 1,
                        "label": "Mode de paiement",
                        "options": [
                            {"label": "VISA", "value": "VISA"},
                            {"label": "CB", "value": "CB"},
                            {"label": "Mastercard", "value": "Mastercard"},
                            {"label": "Espèces", "value": "Espèces"}
                        ],
                        "rules": {
                            "max": 16,
                            "required": True
                        }
                    }
                ]
            },
            {
                "title": "3. Totaux & TVA",
                "position": "after_items",
                "fields": [
                    {
                        "key": "total",
                        "kind": "text",
                        "span": 1,
                        "label": "Total TTC (€)",
                        "placeholder": "820,00",
                        "rules": {
                            "required": True
                        }
                    },
                    {
                        "key": "monnaie",
                        "kind": "text",
                        "span": 1,
                        "label": "Rendu monnaie (€)",
                        "placeholder": "0,00",
                        "advanced": True
                    },
                    {
                        "key": "tva_rate",
                        "kind": "text",
                        "span": 1,
                        "label": "Taux de TVA (%)",
                        "placeholder": "20,00",
                        "advanced": True
                    }
                ]
            }
        ],
        "itemBlank": {
            "sku": "JWWJ156916",
            "desc": "SUMMER, WALK LOADERS, FAE8124",
            "qte": "1",
            "prix": "820,00"
        },
        "itemColumns": [
            {
                "key": "sku",
                "label": "Réf / Article",
                "rules": {
                    "max": 16
                }
            },
            {
                "key": "desc",
                "label": "Désignation",
                "rules": {
                    "max": 48
                }
            },
            {
                "key": "qte",
                "label": "Qté",
                "rules": {
                    "max": 8
                }
            },
            {
                "key": "prix",
                "label": "Prix TTC (€)",
                "rules": {
                    "max": 12
                }
            }
        ],
        "itemsConfig": {
            "key": "items",
            "label": "Articles (6 maximum)",
            "columns": [
                {
                    "key": "sku",
                    "kind": "text",
                    "label": "Réf / Article",
                    "required": True
                },
                {
                    "key": "desc",
                    "kind": "text",
                    "label": "Désignation",
                    "required": True
                },
                {
                    "key": "qte",
                    "kind": "text",
                    "label": "Qté",
                    "required": True
                },
                {
                    "key": "prix",
                    "kind": "text",
                    "label": "Prix TTC (€)",
                    "required": True
                }
            ],
            "enabled": True,
            "maxItems": 6,
            "blankItem": {
                "sku": "JWWJ156916",
                "desc": "SUMMER, WALK LOADERS, FAE8124",
                "qte": "1",
                "prix": "820,00"
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
                    "label": "Logo Loro Piana",
                    "section": "header"
                },
                {
                    "id": "header_store",
                    "label": "Coordonnées boutique",
                    "section": "header"
                },
                {
                    "id": "header_title",
                    "label": "Titre document (Reçu)",
                    "section": "header"
                },
                {
                    "id": "header_refs",
                    "label": "Références ticket, caisse et caissier",
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de ticket complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_columns",
                    "label": "En-tête colonnes tableau",
                    "section": "middle"
                },
                {
                    "id": "middle_rows",
                    "label": "Lignes d articles",
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Totaux et TVA",
                    "section": "middle"
                },
                {
                    "id": "middle_pay",
                    "label": "Mode de règlement et Monnaie",
                    "section": "middle"
                },
                {
                    "id": "middle_line",
                    "label": "Ligne de séparation basse",
                    "section": "middle"
                }
            ],
            "visible": {
                "header": True,
                "middle": True,
                "middle_pay": True,
                "header_logo": True,
                "header_refs": True,
                "middle_line": True,
                "middle_rows": True,
                "header_store": True,
                "header_title": True,
                "middle_totals": True,
                "middle_columns": True
            },
            "sections": [
                {
                    "id": "header",
                    "label": "En-tête boutique"
                },
                {
                    "id": "middle",
                    "label": "Articles et Paiement"
                }
            ]
        }
    }
