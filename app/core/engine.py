from app.models.schemas import UserProfile, BenefitEvaluation, CriterionResult
from app.core.variables import RuleVariables
from app.models.rules_config import RAW_RULES_CONFIG

class BusinessRuleEvaluator:
    @staticmethod
    def _evaluate_condition_value(config_key: str, expected_val, actual_val) -> bool:
        """Infers the mathematical operator from the JSON key syntax."""
        if actual_val is None:
            return False
            
        # Handle IN operator (list of allowed values)
        if isinstance(expected_val, list) and not isinstance(expected_val[0], dict):
            return actual_val in expected_val
            
        # Handle exact match (Booleans and Strings)
        if isinstance(expected_val, (bool, str)):
            return actual_val == expected_val
            
        # Handle inferred numerical ranges
        if isinstance(expected_val, (int, float)):
            if "min" in config_key or "under_age" in config_key:
                return actual_val >= expected_val if "min" in config_key else actual_val <= expected_val
            return actual_val == expected_val
            
        return False

    @staticmethod
    def _evaluate_block(conditions: dict | list, variables_map: dict) -> bool:
        """Recursively parses logical blocks (AND, OR, ANY) from the JSON."""
        
        # If it's a list (used inside 'or' blocks), at least one dict must pass
        if isinstance(conditions, list):
            return any(BusinessRuleEvaluator._evaluate_block(sub_cond, variables_map) for sub_cond in conditions)

        # Iterate through key-value pairs (Implicit AND within a dict)
        for key, value in conditions.items():
            if key in ["any", "or"]:
                # OR logic: Return True if at least one sub-condition passes
                block_passed = False
                if isinstance(value, dict):
                    block_passed = any(BusinessRuleEvaluator._evaluate_block({k: v}, variables_map) for k, v in value.items())
                elif isinstance(value, list):
                    block_passed = BusinessRuleEvaluator._evaluate_block(value, variables_map)
                
                if not block_passed:
                    return False
            else:
                # Standard explicit condition evaluation
                actual_val = variables_map.get(key)
                if not BusinessRuleEvaluator._evaluate_condition_value(key, value, actual_val):
                    return False
                    
        return True

    @staticmethod
    def run(profile: UserProfile) -> list[BenefitEvaluation]:
        variables_map = RuleVariables.extract(profile)
        evaluations = []

        rules_dict = RAW_RULES_CONFIG.get("rules", {})
        
        # Map JSON keys to clean output names
        benefit_names = {
            "prime_activite": "Prime d'activité",
            "ame": "Aide Médicale de l'État (AME)",
            "allocations_familiales": "Allocations Familiales"
        }
        benefit_info_urls = {
            "prime_activite": "https://www.service-public.gouv.fr/particuliers/vosdroits/R42724",
            "ame": "https://www.ameli.fr/sites/default/files/formulaires/formulaire-ame-s3720i-homologue-2026.pdf",
            "allocations_familiales": "https://www.service-public.gouv.fr/particuliers/vosdroits/R1292"
        }

        for benefit_key, rules_list in rules_dict.items():
            criteria_results = []
            benefit_eligible = True

            # Evaluate each rule object (PA_1, PA_2...)
            for rule in rules_list:
                rule_name = rule.get("name", rule.get("id"))
                conditions = rule.get("conditions", {})
                
                # Check if the entire rule block passes
                status = BusinessRuleEvaluator._evaluate_block(conditions, variables_map)
                
                if not status:
                    benefit_eligible = False

                criteria_results.append(CriterionResult(
                    criterion_name=f"[{rule.get('id')}] {rule_name}",
                    status=status,
                    details="Validé" if status else "Échec des conditions requises."
                ))

            evaluations.append(BenefitEvaluation(
                benefit_name=benefit_names.get(benefit_key, benefit_key),
                eligible=benefit_eligible,
                estimated_amount=None,  # Amounts stripped to focus on pure eligibility per your JSON
                info_url=benefit_info_urls.get(benefit_key) if benefit_eligible else None,
                criteria_details=criteria_results
            ))

        return evaluations