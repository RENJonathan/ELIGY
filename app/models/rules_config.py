BENEFITS_RULES_SPECIFICATION = {
    "Prime d'activité": {
        "base_amount": 600.0,
        "calculate_amount": True,
        "criteria": [
            {
                "name": "Condition d'âge minimal (18 ans)",
                "variable": "age",
                "operator": "greater_than_or_equal_to",
                "value": 18
            },
            {
                "name": "Exclusion des travailleurs détachés",
                "variable": "is_detached_worker",
                "operator": "equal_to",
                "value": False
            },
            {
                "name": "Résidence stable en France (9 mois minimum par an)",
                "variable": "has_stable_yearly_residence",
                "operator": "equal_to",
                "value": True
            },
            {
                "name": "Régularité des conditions de séjour (Nationalité / Titre de travail)",
                "variable": "has_valid_administrative_status",
                "operator": "equal_to",
                "value": True
            },
            {
                "name": "Revenus d'activité conformes au statut (Seuil Étudiant/Apprenti si applicable)",
                "variable": "passes_activity_income_threshold",
                "operator": "equal_to",
                "value": True
            },
            {
                "name": "Plafond de ressources globales du foyer",
                "variable": "household_total_resources",
                "operator": "less_than_or_equal_to",
                "value": 1900.0
            }
        ]
    }
}