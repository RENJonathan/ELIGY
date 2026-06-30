from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_scenario_1_salarie_francais_eligible():
    """Scénario 1: Citoyen français, salarié, revenus modestes -> Doit être éligible."""
    payload = {
        "identity": {
            "age": 25,
            "nationality_zone": "FR",
            "months_in_france_per_year": 12,
            "months_of_stable_residence": 120,  
            "is_detached_worker": False,
            "has_stable_residence_right": True,
            "has_work_permitting_visa": True,
            "years_of_regular_residence": 10,
            "has_resident_card": False,
            "is_refugee_or_protected": False,
            "is_stateless": False,
            "is_isolated_parent_with_child_under_3": False
        },
        "income": {
            "monthly_net_social_income": 1200.0,
            "household_total_resources": 1200.0
        },
        "family": {
            "dependent_children_count": 0
        },
        "current_status": "employee"  
    }
    
    response = client.post("/api/v1/evaluate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    prime_info = next(b for b in data["user_eligible_benefits"] if b["benefit_name"] == "Prime d'activité")
    assert prime_info["eligible"] is True
    assert "info_url" in prime_info
    assert prime_info["info_url"].startswith("http")

def test_scenario_2_etudiant_sous_seuil_ineligible():
    """Scénario 2: Étudiant gagnant 600€ (inférieur au seuil de 1117.26€) -> Doit être refusé."""
    payload = {
        "identity": {
            "age": 21,
            "nationality_zone": "FR",
            "months_in_france_per_year": 12,
            "months_of_stable_residence": 60,  
            "is_detached_worker": False,
            "has_stable_residence_right": True,
            "has_work_permitting_visa": True,
            "years_of_regular_residence": 5,
            "has_resident_card": False,
            "is_refugee_or_protected": False,
            "is_stateless": False,
            "is_isolated_parent_with_child_under_3": False
        },
        "income": {
            "monthly_net_social_income": 600.0,
            "household_total_resources": 600.0
        },
        "family": {
            "dependent_children_count": 0
        },
        "current_status": "student"
    }
    
    response = client.post("/api/v1/evaluate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    prime_info = next(b for b in data["user_eligible_benefits"] if b["benefit_name"] == "Prime d'activité")
    
    # Doit être False à cause de la condition de revenu étudiant (PA_9)
    assert prime_info["eligible"] is False 
    
    # On vérifie que le critère PA_9 a bien échoué
    income_criterion = next(c for c in prime_info["criteria_details"] if "PA_9" in c["criterion_name"])
    assert income_criterion["status"] is False

def test_scenario_3_etranger_hors_ue_sans_anciennete_ineligible():
    """Scénario 3: Étranger hors-UE, réside depuis 2 ans seulement, sans statut réfugié -> Inéligible."""
    payload = {
        "identity": {
            "age": 30,
            "nationality_zone": "OTHER",
            "months_in_france_per_year": 12,
            "months_of_stable_residence": 24,  
            "is_detached_worker": False,
            "has_stable_residence_right": False,
            "has_work_permitting_visa": True,
            "years_of_regular_residence": 2,  
            "has_resident_card": False,
            "is_refugee_or_protected": False, 
            "is_stateless": False,
            "is_isolated_parent_with_child_under_3": False
        },
        "income": {
            "monthly_net_social_income": 1300.0,
            "household_total_resources": 1300.0
        },
        "family": {
            "dependent_children_count": 0
        },
        "current_status": "employee"  
    }
    
    response = client.post("/api/v1/evaluate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    prime_info = next(b for b in data["user_eligible_benefits"] if b["benefit_name"] == "Prime d'activité")
    assert prime_info["eligible"] is False