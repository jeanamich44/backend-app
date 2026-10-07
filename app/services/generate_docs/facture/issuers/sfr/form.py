def get_form_schema() -> dict:
    return {
        "metadata": {
            "logo": "/logos/sfr.svg",
            "title": "GÉNÉRATEUR FACTURE SFR",
            "subtitle": "Facture officielle SFR Box & Mobile",
            "apiBase": "/api/generate-docs/facture/sfr",
            "backHref": "/services/generate-docs/facture",
            "backLabel": "Retour aux factures",
            "category": "facture",
            "headerBg": "bg-white border-red-500/30",
            "priceKey": "sfr",
            "itemKey": "items",
            "itemLabel": "3. Lignes & Prestations",
            "maxItems": 3,
            "generateLabel": "Générer la facture",
            "filenameTemplate": "Facture_SFR.pdf"
        },
        "defaults": {
            "nom": "Martin",
            "prenom": "Lucas",
            "adresse": "12 Rue des Fleurs",
            "cp": "75011",
            "ville": "Paris",
            "destinataire_nom": "LUCAS MARTIN",
            "destinataire_adresse": "12 Rue des Fleurs",
            "destinataire_cp_ville": "75011 Paris",
            "titulaire_ligne": "LUCAS MARTIN",
            "num_compte_client": "2LH5L",
            "date_facture": "2026-09-01",
            "num_facture": "169793",
            "montant_ht": "6.25",
            "montant_tva": "1.25",
            "taux_tva": "20.0 %",
            "total_ttc": "7.50",
            "solde_ht": "0.00",
            "solde_ttc": "0.00",
            "net_a_payer_ht": "6.25",
            "net_a_payer_ttc": "7.50",
            "total_facture_ht": "6.25",
            "total_facture_ttc": "7.50",
            "mention_encaissement": "TVA acquittée sur les encaissements.",
            "footer_note": "Pour toute réclamation, contactez notre service client. Si aucun accord n'est trouvé, vous pouvez saisir le médiateur.",
            "sepa_ligne1": "Le prélèvement de votre facture se fera sur le compte no FPELFR21 FR76XXXXXXXXXXXXXXX5545 par l'ICS no xxx",
            "sepa_ligne2": "conformément à votre Mandat de prélèvement SEPA référencé 2LH5L-00000 le 2026-10-01.",
            "service_faq_url": "www.sfr-discover.fr",
            "service_phone": "Numéro du service client : 09 70 83 10 23 ou 1023 depuis une ligne",
            "service_siege": "Siège social : 16 rue du Général Alain de Boissieu 75015 Paris ",
            "company_name": "SFR Discover - Service Client",
            "company_address": "16 rue du Général Alain de Boissieu 75015 Paris",
            "company_capital_rcs": "SA au capital de 3 423 265 720 Euro - RCS de Paris 343 059 564",
            "company_tva_ape": "N° de TVA intracommunautaire: FR 71 343 059 564 - APE : 6120Z",
            "items": [
                {
                    "numero_ligne": "06 12 34 56 78",
                    "description": "Pénalités de retard pour échec de prélèvement: 7.5 €",
                    "date": "2026-09-01",
                    "montant_ttc": "7.50"
                }
            ]
        },
        "version": 2,
        "sections": [
            {
                "title": "1. Titulaire & Coordonnées",
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
                    }
                ]
            },
            {
                "title": "2. Références Facture & Compte",
                "fields": [
                    {
                        "key": "date_facture",
                        "label": "Date de facture",
                        "kind": "date",
                        "dateFormat": "dash"
                    },
                    {
                        "key": "num_facture",
                        "label": "N° de facture"
                    },
                    {
                        "key": "num_compte_client",
                        "label": "N° compte client"
                    }
                ]
            },
            {
                "title": "4. Récapitulatif & Règlement",
                "position": "after_items",
                "fields": [
                    {
                        "key": "montant_ht",
                        "label": "Montant HT soumis à TVA (€)"
                    },
                    {
                        "key": "total_ttc",
                        "label": "Montant total facture TTC (€)"
                    },
                    {
                        "key": "montant_tva",
                        "label": "Montant total TVA (€)",
                        "advanced": True
                    },
                    {
                        "key": "taux_tva",
                        "label": "Taux TVA",
                        "advanced": True
                    },
                    {
                        "key": "solde_ttc",
                        "label": "Solde TTC avant facturation (€)",
                        "advanced": True
                    },
                    {
                        "key": "sepa_ligne1",
                        "label": "Mandat SEPA (compte prélevé)",
                        "advanced": True
                    }
                ]
            }
        ],
        "itemColumns": [
            {
                "key": "numero_ligne",
                "label": "N° de ligne"
            },
            {
                "key": "description",
                "label": "Description"
            },
            {
                "key": "date",
                "label": "Date",
                "kind": "date"
            },
            {
                "key": "montant_ttc",
                "label": "Montant TTC"
            }
        ],
        "customLayout": {
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
            ],
            "blocks": [
                {
                    "id": "header",
                    "label": "En-tête complet",
                    "master": True,
                    "section": "header"
                },
                {
                    "id": "header_logo",
                    "label": "Logo SFR",
                    "section": "header"
                },
                {
                    "id": "header_service",
                    "label": "Bloc Service client",
                    "section": "header"
                },
                {
                    "id": "header_company",
                    "label": "Bloc Société SFR Discover",
                    "section": "header"
                },
                {
                    "id": "header_account",
                    "label": "Bloc Compte & N° Facture",
                    "section": "header"
                },
                {
                    "id": "header_recipient",
                    "label": "Bloc Destinataire",
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_recap",
                    "label": "Tableau récapitulatif montants",
                    "section": "middle"
                },
                {
                    "id": "middle_banner",
                    "label": "Bandeau rouge titre facture",
                    "section": "middle"
                },
                {
                    "id": "middle_table",
                    "label": "Tableau des prestations",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_notes",
                    "label": "Mentions légales & Réclamations",
                    "section": "footer"
                },
                {
                    "id": "footer_sepa",
                    "label": "Encadré mandat de prélèvement SEPA",
                    "section": "footer"
                }
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_service": True,
                "header_company": True,
                "header_account": True,
                "header_recipient": True,
                "middle": True,
                "middle_recap": True,
                "middle_banner": True,
                "middle_table": True,
                "footer": True,
                "footer_notes": True,
                "footer_sepa": True
            }
        }
    }
