# Configuration based on the user's JSON structure, logically corrected for mutually exclusive branches.

RAW_RULES_CONFIG = {
  "rules": {
    "prime_activite": [
      {
        "id": "PA_1",
        "name": "Age minimum",
        "conditions": { "age_min": 18 },
        "result": { "eligible": True }
      },
      {
        "id": "PA_2",
        "name": "Residence stable France",
        "conditions": {
          "min_months_residence_per_year": 9,
          "country_of_residence": "FR"
        },
        "result": { "eligible": True }
      },
      {
        "id": "PA_3",
        "name": "Exclusion travailleur detache",
        "conditions": { "detached_worker": False },
        "result": { "eligible": True }
      },
      {
        "id": "PA_4_5_6_7",
        "name": "Conditions de Nationalité et Séjour (Mutuellement exclusives)",
        "conditions": {
          "or": [
            { "nationality_zone": "FR" },
            { 
              "nationality_zone": "UE_EEE_CH", 
              "right_to_stay": True 
            },
            {
              "nationality_zone": "OTHER",
              "has_valid_residence_permit": True,
              "permit_authorizes_work": True,
              "or": [
                  { "years_of_residence_in_france_min": 5 },
                  { "any": {
                      "has_resident_card": True,
                      "status_refugee": True,
                      "status_subsidiary_protection": True,
                      "status_stateless": True,
                      "single_parent_with_child_under_3": True
                  }}
              ]
            }
          ]
        },
        "result": { "eligible": True }
      },
      {
        "id": "PA_8",
        "name": "Activité professionnelle",
        "conditions": {
          "employment_required": True,
          "activity_type_allowed": [
            "employee",
            "self_employed",
            "partial_unemployment",
            "technical_unemployment"
          ]
        },
        "result": { "eligible": True }
      },
      {
        "id": "PA_9",
        "name": "Etudiant apprenti stagiaire seuil revenu (Ignoré si non étudiant)",
        "conditions": {
          "or": [
              { "student_status": False },
              { "student_status": True, "monthly_net_income_min": 1117.0 }
          ]
        },
        "result": { "eligible": True }
      }
    ],

    "ame": [
      {
        "id": "AME_1",
        "name": "Residence stable 3 mois",
        "conditions": { "min_months_residence": 3 },
        "result": { "eligible": True }
      },
      {
        "id": "AME_2",
        "name": "Situation irreguliere",
        "conditions": { "has_valid_residence_permit": False },
        "result": { "eligible": True }
      },
      {
        "id": "AME_3",
        "name": "Non éligible assurance maladie classique",
        "conditions": { "eligible_to_health_insurance": False },
        "result": { "eligible": True }
      },
      {
        "id": "AME_4",
        "name": "Ressources sous plafond",
        "conditions": { "household_income_under_threshold": True },
        "result": { "eligible": True }
      }
    ],

    "allocations_familiales": [
      {
        "id": "AF_1",
        "name": "Minimum 2 enfants",
        "conditions": { "children_count_min": 2 },
        "result": { "eligible": True }
      },
      {
        "id": "AF_2",
        "name": "Enfants moins de 20 ans",
        "conditions": { "children_all_under_age": 20 },
        "result": { "eligible": True }
      },
      {
        "id": "AF_3",
        "name": "Residence stable France",
        "conditions": {
          "residence_stable": True,
          "country_of_residence": "FR"
        },
        "result": { "eligible": True }
      },
      {
        "id": "AF_4",
        "name": "Nationalité ou droit séjour",
        "conditions": {
          "or": [
            { "nationality_zone": "FR" },
            { "right_to_stay": True }
          ]
        },
        "result": { "eligible": True }
      }
    ]
  }
}