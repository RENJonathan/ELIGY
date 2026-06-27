from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_scenario_af_eligible_classique():
    """Scénario 1: Famille française, 2 enfants de 10 ans, résidant en France -> Éligible."""
    payload = {
        "identity": {
            "age": 40,
            "country_of_residence": "FR",
            "nationality_zone": "FR",
            "months_in_france_per_year": 12,
            "months_of_stable_residence": 120,
            "is_detached_worker": False,
            "has_stable_residence_right": True,
            "has_work_permitting_visa": True,
            "years_of_regular_residence": 40,
            "has_resident_card": False,
            "is_refugee_or_protected": False,
            "is_stateless": False,
            "is_isolated_parent_with_child_under_3": False
        },
        "income": {
            "monthly_net_social_income": 2500.0,
            "household_total_resources": 2500.0
        },
        "family": {
            "dependent_children_count": 2,
            "children_max_age": 10
        },
        "current_status": "employee"
    }
    
    response = client.post("/api/v1/evaluate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    af_info = next(b for b in data["user_eligible_benefits"] if "Allocations" in b["benefit_name"])
    assert af_info["eligible"] is True

def test_scenario_af_refuse_un_seul_enfant():
    """Scénario 2: Famille avec 1 seul enfant -> Inéligible (Minimum 2 requis)."""
    payload = {
        "identity": {
            "age": 35,
            "country_of_residence": "FR",
            "nationality_zone": "FR",
            "months_in_france_per_year": 12,
            "months_of_stable_residence": 60,
            "is_detached_worker": False,
            "has_stable_residence_right": True,
            "has_work_permitting_visa": True,
            "years_of_regular_residence": 35,
            "has_resident_card": False,
            "is_refugee_or_protected": False,
            "is_stateless": False,
            "is_isolated_parent_with_child_under_3": False
        },
        "income": {
            "monthly_net_social_income": 2000.0,
            "household_total_resources": 2000.0
        },
        "family": {
            "dependent_children_count": 1,  # Bloquant
            "children_max_age": 5
        },
        "current_status": "employee"
    }
    
    response = client.post("/api/v1/evaluate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    af_info = next(b for b in data["user_eligible_benefits"] if "Allocations" in b["benefit_name"])
    assert af_info["eligible"] is False
    
    criterion = next(c for c in af_info["criteria_details"] if "AF_1" in c["criterion_name"])
    assert criterion["status"] is False

def test_scenario_af_refuse_enfant_trop_age():
    """Scénario 3: Famille avec 2 enfants, mais l'aîné a 22 ans -> Inéligible."""
    payload = {
        "identity": {
            "age": 50,
            "country_of_residence": "FR",
            "nationality_zone": "FR",
            "months_in_france_per_year": 12,
            "months_of_stable_residence": 240,
            "is_detached_worker": False,
            "has_stable_residence_right": True,
            "has_work_permitting_visa": True,
            "years_of_regular_residence": 50,
            "has_resident_card": False,
            "is_refugee_or_protected": False,
            "is_stateless": False,
            "is_isolated_parent_with_child_under_3": False
        },
        "income": {
            "monthly_net_social_income": 3000.0,
            "household_total_resources": 3000.0
        },
        "family": {
            "dependent_children_count": 2,
            "children_max_age": 22  # Bloquant (limite: 20 ans)
        },
        "current_status": "self_employed"
    }
    
    response = client.post("/api/v1/evaluate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    af_info = next(b for b in data["user_eligible_benefits"] if "Allocations" in b["benefit_name"])
    assert af_info["eligible"] is False
    
    criterion = next(c for c in af_info["criteria_details"] if "AF_2" in c["criterion_name"])
    assert criterion["status"] is False

def test_scenario_af_eligible_etranger_regulier():
    """Scénario 4: Étranger hors-UE avec droit de séjour valide, 3 enfants -> Éligible."""
    payload = {
        "identity": {
            "age": 38,
            "country_of_residence": "FR",
            "nationality_zone": "OTHER",
            "months_in_france_per_year": 10,
            "months_of_stable_residence": 24,
            "is_detached_worker": False,
            "has_stable_residence_right": True,  # Autorise le passage de AF_4
            "has_work_permitting_visa": True,
            "years_of_regular_residence": 2,
            "has_resident_card": False,
            "is_refugee_or_protected": False,
            "is_stateless": False,
            "is_isolated_parent_with_child_under_3": False
        },
        "income": {
            "monthly_net_social_income": 1800.0,
            "household_total_resources": 1800.0
        },
        "family": {
            "dependent_children_count": 3,
            "children_max_age": 14
        },
        "current_status": "employee"
    }
    
    response = client.post("/api/v1/evaluate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    af_info = next(b for b in data["user_eligible_benefits"] if "Allocations" in b["benefit_name"])
    assert af_info["eligible"] is True