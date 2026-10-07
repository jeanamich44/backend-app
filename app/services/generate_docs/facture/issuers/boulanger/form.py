def get_form_schema() -> dict:
    return {
        "defaults": {
            "cp": "75011",
            "nom": "Martin",
            "mode": "en_ligne",
            "items": [
                {
                    "nom": "PACK ADEQWAT Powerbank + Chargeur + C",
                    "qte": "1",
                    "code": "0008010892",
                    "pu_ttc": "49,97",
                    "ecopart": "0,02",
                    "tva_taux": "20,00",
                    "total_ttc": "49,97",
                    "dispo_pieces": "Pas de pièce disponible",
                    "garantie_reparation": "Garantie Réparation jusqu'au 19.12.2025"
                }
            ],
            "ville": "Paris",
            "prenom": "Lucas",
            "adresse": "12 Rue des Fleurs",
            "dont_tva": "9,00",
            "store_cp": "59810",
            "total_ht": "44,99",
            "store_nom": "BOULANGER WWW.BOULANGER.COM",
            "store_tel": "03 86 42 53 08",
            "total_ttc": "53,98",
            "client_num": "29468065",
            "client_tel": "06 12 34 56 78",
            "store_rue1": "CRT - BP137",
            "store_rue2": "AV DE LA MOTTE",
            "barcode_val": "0008010892",
            "facture_num": "F905 FQ09058-23/002",
            "store_siret": "34738457002017",
            "store_ville": "LESQUIN",
            "dont_ecopart": "0,02",
            "facture_date": "09/09/2026",
            "facture_time": "19:23",
            "extra_line_nom": "BOULANGER FRAIS DE PORT",
            "reglement_mode": "Carte Bancaire",
            "extra_line_total": "3,99",
            "extra_line_pu_ttc": "3,99",
            "reglement_montant": "53,98"
        },
        "metadata": {
            "logo": "/logos/boulanger.svg",
            "title": "GÉNÉRATEUR FACTURE BOULANGER",
            "apiBase": "/api/generate-docs/facture/boulanger",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "category": "facture",
            "headerBg": "bg-white border-orange-500/30",
            "maxItems": 3,
            "priceKey": "boulanger",
            "subtitle": "Document PDF Boulanger officiel (En ligne & Magasin)",
            "backLabel": "Retour aux factures",
            "itemBlank": {
                "nom": "",
                "qte": "1",
                "code": "",
                "pu_ttc": "0,00",
                "ecopart": "0,00",
                "tva_taux": "20,00",
                "total_ttc": "0,00",
                "dispo_pieces": "",
                "garantie_reparation": ""
            },
            "itemLabel": "5. Articles",
            "logoClass": "scale-110 md:scale-120",
            "generateLabel": "Générer la facture",
            "filenameTemplate": "Facture_Boulanger.pdf"
        },
        "sections": [
            {
                "title": "1. Version de facture",
                "fields": [
                    {
                        "key": "mode",
                        "kind": "select",
                        "span": 2,
                        "label": "Modèle de facture",
                        "options": [
                            {
                                "label": "Commande en ligne (Boulanger.com)",
                                "value": "en_ligne"
                            },
                            {
                                "label": "Achat en magasin (Boulanger Magasin)",
                                "value": "magasin"
                            }
                        ]
                    }
                ]
            },
            {
                "title": "2. Facturation",
                "fields": [
                    {
                        "key": "nom",
                        "label": "Nom"
                    },
                    {
                        "key": "prenom",
                        "label": "Prénom"
                    },
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
                    },
                    {
                        "key": "client_num",
                        "label": "N° client",
                        "advanced": True
                    },
                    {
                        "key": "client_tel",
                        "label": "Téléphone client",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "3. Magasin / Émetteur",
                "advanced": True,
                "fields": [
                    {
                        "key": "store_nom",
                        "label": "Nom du magasin",
                        "advanced": True
                    },
                    {
                        "key": "store_rue1",
                        "label": "Adresse ligne 1",
                        "advanced": True
                    },
                    {
                        "key": "store_rue2",
                        "label": "Adresse ligne 2",
                        "advanced": True
                    },
                    {
                        "key": "store_cp",
                        "label": "Code postal",
                        "advanced": True
                    },
                    {
                        "key": "store_ville",
                        "label": "Ville",
                        "advanced": True
                    },
                    {
                        "key": "store_siret",
                        "label": "N° SIRET",
                        "advanced": True
                    },
                    {
                        "key": "store_tel",
                        "label": "Téléphone",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "4. Facture & Date",
                "fields": [
                    {
                        "key": "facture_num",
                        "label": "N° de facture"
                    },
                    {
                        "key": "facture_date",
                        "kind": "date",
                        "label": "Date facture",
                        "dateFormat": "slash"
                    },
                    {
                        "key": "facture_time",
                        "kind": "time",
                        "label": "Heure facture",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "5. Totaux & Règlement",
                "position": "after_items",
                "fields": [
                    {
                        "key": "total_ht",
                        "label": "Total HT",
                        "advanced": True
                    },
                    {
                        "key": "total_ttc",
                        "label": "Total TTC"
                    },
                    {
                        "key": "dont_tva",
                        "label": "Dont TVA",
                        "advanced": True
                    },
                    {
                        "key": "dont_ecopart",
                        "label": "Dont Éco-part",
                        "advanced": True
                    },
                    {
                        "key": "reglement_mode",
                        "label": "Mode de règlement"
                    },
                    {
                        "key": "reglement_montant",
                        "label": "Montant réglé"
                    },
                    {
                        "key": "extra_line_nom",
                        "label": "Ligne supp. (ex: Frais de port)",
                        "advanced": True
                    },
                    {
                        "key": "extra_line_total",
                        "label": "Montant ligne supp.",
                        "advanced": True
                    }
                ]
            }
        ],
        "itemBlank": {
            "nom": "",
            "qte": "1",
            "code": "",
            "pu_ttc": "0,00",
            "ecopart": "0,00",
            "tva_taux": "20,00",
            "total_ttc": "0,00",
            "dispo_pieces": "",
            "garantie_reparation": ""
        },
        "itemColumns": [
            {
                "key": "nom",
                "label": "Désignation"
            },
            {
                "key": "code",
                "label": "Réf/Code"
            },
            {
                "key": "qte",
                "label": "Qté"
            },
            {
                "key": "pu_ttc",
                "label": "Prix unitaire TTC"
            },
            {
                "key": "total_ttc",
                "label": "Total TTC"
            },
            {
                "key": "tva_taux",
                "label": "TVA %",
                "advanced": True
            },
            {
                "key": "ecopart",
                "label": "Éco-part",
                "advanced": True
            },
            {
                "key": "garantie_reparation",
                "label": "Garantie",
                "advanced": True
            },
            {
                "key": "dispo_pieces",
                "label": "Pièces détachées",
                "advanced": True
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
                    "id": "header_lateral_logo",
                    "label": "Logo Boulanger",
                    "section": "header"
                },
                {
                    "id": "header_lateral_barcode",
                    "label": "Code-barres latéral",
                    "section": "header"
                },
                {
                    "id": "header_lateral_sidebar",
                    "label": "Barre latérale (app / contact)",
                    "section": "header"
                },
                {
                    "id": "header_title",
                    "label": "Numéro & date de facture",
                    "section": "header"
                },
                {
                    "id": "header_addresses",
                    "label": "Adresses magasin & client",
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_table_header",
                    "label": "En-tête du tableau articles",
                    "section": "middle"
                },
                {
                    "id": "middle_articles",
                    "label": "Lignes d'articles",
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Totaux HT, TVA & TTC",
                    "section": "middle"
                },
                {
                    "id": "middle_payment",
                    "label": "Mode et montant du règlement",
                    "section": "middle"
                },
                {
                    "id": "middle_notice",
                    "label": "Notices et garanties légales",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_company",
                    "label": "Mentions société Boulanger SA",
                    "section": "footer"
                },
                {
                    "id": "footer_legal",
                    "label": "Conditions générales de vente (bas)",
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "footer_legal": True,
                "header_title": True,
                "middle_notice": True,
                "middle_totals": True,
                "footer_company": True,
                "middle_payment": True,
                "middle_articles": True,
                "header_addresses": True,
                "header_lateral_logo": True,
                "middle_table_header": True,
                "header_lateral_barcode": True,
                "header_lateral_sidebar": True
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
