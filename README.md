

```
zizofa-allocs-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # Initialisation FastAPI et inclusion des routeurs
│   │
│   ├── api/                     # Couche transport (Endpoints HTTP)
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   └── evaluate.py      # Route POST /api/v1/evaluate
│   │
│   ├── core/                    # Logique métier pure (Moteur de règles)
│   │   ├── __init__.py
│   │   ├── engine.py            # BusinessRuleEvaluator (Interprète)
│   │   └── variables.py         # RuleVariables (Adaptateur de profil)
│   │
│   ├── models/                  # Schémas de données et configurations
│   │   ├── __init__.py
│   │   ├── schemas.py           # Modèles de validation Pydantic
│   │   └── rules_config.py      # Registre de règles (Déclaratif JSON)
│   │
│   └── tests/                   # Suite de tests automatisés (Profils types)
│       ├── __init__.py
│       ├── test_prime_activite.py
│       └── test_ame.py
│
├── requirements.txt             # Dépendances (fastapi, uvicorn, pydantic)
└── README.md
```