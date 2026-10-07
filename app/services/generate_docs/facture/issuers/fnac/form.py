def get_form_schema() -> dict:
    return {
        "version": 6,
        "defaults": {
            "nref": "2027880107 - MLUCAS -FND",
            "items": [
                {
                    "ean": "3001100110011",
                    "nom": "Casque audio sans fil Bluetooth, autonomie 30 h.",
                    "qte": "1",
                    "pu_ht": "100.00",
                    "eco_ht": "0.00",
                    "pieces": "",
                    "pu_ttc": "120.00",
                    "serial": "",
                    "eco_ttc": "0.00",
                    "garantie": "",
                    "subtitle": "",
                    "reference": "1001101",
                    "remise_ht": "0.00",
                    "pu_brut_ht": "100.00",
                    "distribution": ""
                }
            ],
            "total": "120.00",
            "en_ligne": "true",
            "frais_ht": "0.00",
            "store_l1": "ZONE LOGISTIQUE NORD",
            "store_l2": "91000 EVRY",
            "store_l3": "FRANCE",
            "tva_code": "I",
            "tva_rate": "20.00",
            "matricule": "7000575",
            "store_nom": "FNAC DIRECT",
            "tva_frais": "0.00",
            "num_facture": "2027880107",
            "livraison_cp": "75011",
            "num_commande": "BXU7ZFTY2SUE2",
            "payment_mode": "Carte bancaire",
            "livraison_nom": "Martin",
            "facturation_cp": "75011",
            "livraison_pays": "FR",
            "facturation_nom": "Martin",
            "livraison_email": "martin.lucas@gmail.com",
            "livraison_ville": "Paris",
            "pays_expedition": "Pays d'expédition : FRANCE (Union Européenne) – Shipping country : FRANCE (European Union)",
            "facturation_pays": "FR",
            "livraison_prenom": "Lucas",
            "facturation_email": "martin.lucas@gmail.com",
            "facturation_ville": "Paris",
            "livraison_adresse": "12 Rue des Fleurs",
            "facturation_prenom": "Lucas",
            "livraison_cp_ville": "75011 Paris",
            "facturation_adresse": "12 Rue des Fleurs",
            "facturation_cp_ville": "75011 Paris"
        },
        "metadata": {
            "logo": "/logos/fnac.svg",
            "title": "GÉNÉRATEUR FACTURE FNAC",
            "apiBase": "/api/generate-docs/facture/fnac",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "category": "facture",
            "headerBg": "bg-white border-yellow-500/30",
            "maxItems": 12,
            "priceKey": "fnac",
            "subtitle": "Document PDF Fnac officiel",
            "backLabel": "Retour aux factures",
            "itemLabel": "6. Articles",
            "generateLabel": "Générer la facture",
            "filenameTemplate": "Facture_Fnac.pdf"
        },
        "sections": [
            {
                "title": "1. Version de facture",
                "fields": [
                    {
                        "key": "en_ligne",
                        "kind": "select",
                        "span": 2,
                        "label": "Modèle de facture",
                        "options": [
                            {
                                "label": "Commande en ligne (Fnac.com)",
                                "value": "true"
                            },
                            {
                                "label": "Achat en magasin (Fnac Magasin)",
                                "value": "false"
                            }
                        ]
                    }
                ]
            },
            {
                "title": "2. Livraison",
                "fields": [
                    {
                        "key": "livraison_nom",
                        "label": "Nom"
                    },
                    {
                        "key": "livraison_prenom",
                        "label": "Prénom"
                    },
                    {
                        "key": "livraison_adresse",
                        "label": "Adresse"
                    },
                    {
                        "key": "livraison_cp",
                        "label": "Code postal"
                    },
                    {
                        "key": "livraison_ville",
                        "label": "Ville"
                    },
                    {
                        "key": "livraison_email",
                        "label": "Email"
                    },
                    {
                        "key": "livraison_pays",
                        "kind": "country",
                        "label": "Pays",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "3. Facturation",
                "fields": [
                    {
                        "key": "facturation_nom",
                        "label": "Nom"
                    },
                    {
                        "key": "facturation_prenom",
                        "label": "Prénom"
                    },
                    {
                        "key": "facturation_adresse",
                        "label": "Adresse"
                    },
                    {
                        "key": "facturation_cp",
                        "label": "Code postal"
                    },
                    {
                        "key": "facturation_ville",
                        "label": "Ville"
                    },
                    {
                        "key": "facturation_email",
                        "label": "Email"
                    },
                    {
                        "key": "facturation_pays",
                        "kind": "country",
                        "label": "Pays",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "4. Magasin / entrepôt",
                "advanced": True,
                "fields": [
                    {
                        "key": "store_nom",
                        "label": "Nom magasin / enseigne",
                        "advanced": True
                    },
                    {
                        "key": "store_l1",
                        "label": "Ligne adresse 1",
                        "advanced": True
                    },
                    {
                        "key": "store_l2",
                        "label": "Ligne adresse 2",
                        "advanced": True
                    },
                    {
                        "key": "store_l3",
                        "label": "Ligne adresse 3",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "5. Commande",
                "fields": [
                    {
                        "key": "num_commande",
                        "label": "N° de commande"
                    },
                    {
                        "key": "date_commande",
                        "kind": "date",
                        "label": "Date de commande"
                    },
                    {
                        "key": "num_facture",
                        "label": "N° de facture"
                    },
                    {
                        "key": "date_facture",
                        "kind": "date",
                        "label": "Date de facture"
                    },
                    {
                        "key": "payment_mode",
                        "kind": "select",
                        "label": "Mode de règlement",
                        "options": [
                            {
                                "label": "Cheque-cadeau",
                                "value": "Cheque-cadeau"
                            },
                            {
                                "label": "A la caisse",
                                "value": "A la caisse"
                            },
                            {
                                "label": "Carte bancaire",
                                "value": "Carte bancaire"
                            },
                            {
                                "label": "Espèces",
                                "value": "Espèces"
                            },
                            {
                                "label": "Chèque",
                                "value": "Chèque"
                            },
                            {
                                "label": "Virement",
                                "value": "Virement"
                            },
                            {
                                "label": "PayPal",
                                "value": "PayPal"
                            },
                            {
                                "label": "Ticket restaurant",
                                "value": "Ticket restaurant"
                            },
                            {
                                "label": "3x sans frais",
                                "value": "3x sans frais"
                            }
                        ]
                    },
                    {
                        "key": "nref",
                        "label": "N/Réf",
                        "advanced": True
                    },
                    {
                        "key": "matricule",
                        "label": "Matricule vendeur",
                        "advanced": True
                    },
                    {
                        "key": "echeance",
                        "kind": "date",
                        "label": "Échéance",
                        "advanced": True
                    },
                    {
                        "key": "tva_code",
                        "label": "Code TVA",
                        "advanced": True
                    },
                    {
                        "key": "tva_rate",
                        "label": "Taux TVA (%)",
                        "advanced": True
                    },
                    {
                        "key": "frais_ht",
                        "label": "Frais HT",
                        "advanced": True
                    },
                    {
                        "key": "tva_frais",
                        "label": "TVA / frais",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "7. Calculs & Montants",
                "fields": [
                    {
                        "key": "total",
                        "label": "Total à payer"
                    }
                ],
                "position": "after_items"
            }
        ],
        "itemBlank": {
            "ean": "3001100110011",
            "nom": "",
            "qte": "1",
            "pu_ht": "0.00",
            "eco_ht": "0.00",
            "pieces": "",
            "pu_ttc": "0.00",
            "serial": "",
            "eco_ttc": "0.00",
            "garantie": "",
            "subtitle": "",
            "reference": "1001101",
            "remise_ht": "0.00",
            "pu_brut_ht": "0.00",
            "distribution": ""
        },
        "itemColumns": [
            {
                "key": "nom",
                "label": "Libellé"
            },
            {
                "key": "reference",
                "label": "Référence"
            },
            {
                "key": "qte",
                "label": "Quantité"
            },
            {
                "key": "pu_ttc",
                "label": "Prix TTC"
            },
            {
                "key": "pu_ht",
                "label": "Prix unitaire HT",
                "advanced": True
            },
            {
                "key": "pu_brut_ht",
                "label": "Prix brut HT",
                "advanced": True
            },
            {
                "key": "remise_ht",
                "label": "Remise",
                "advanced": True
            },
            {
                "key": "eco_ht",
                "label": "Éco",
                "advanced": True
            },
            {
                "key": "eco_ttc",
                "label": "Éco TTC",
                "advanced": True
            },
            {
                "key": "ean",
                "label": "EAN",
                "advanced": True
            },
            {
                "key": "subtitle",
                "label": "Sous-titre",
                "advanced": True
            },
            {
                "key": "serial",
                "label": "N° de série",
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
                    "id": "header_logo",
                    "label": "Logo Fnac",
                    "section": "header"
                },
                {
                    "id": "header_store",
                    "label": "Magasin / Entrepôt",
                    "section": "header"
                },
                {
                    "id": "header_order",
                    "label": "Références commande",
                    "section": "header"
                },
                {
                    "id": "header_addresses",
                    "label": "Blocs adresses",
                    "section": "header"
                },
                {
                    "id": "header_page",
                    "label": "Numérotation de page",
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
                    "id": "middle_ship",
                    "label": "Mention pays d'expédition",
                    "section": "middle"
                },
                {
                    "id": "middle_vat",
                    "label": "Ventilation TVA",
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Totaux et règlements",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_legal",
                    "label": "Mentions légales",
                    "section": "footer"
                },
                {
                    "id": "footer_help",
                    "label": "Assistance SAV & contacts",
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "middle_vat": True,
                "footer_help": True,
                "header_logo": True,
                "header_page": True,
                "middle_rows": True,
                "middle_ship": True,
                "footer_legal": True,
                "header_order": True,
                "header_store": True,
                "middle_totals": True,
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
