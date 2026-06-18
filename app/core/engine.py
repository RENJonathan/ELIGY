from app.models.schemas import UserProfile, BenefitEvaluation, CriterionResult
from app.core.variables import RuleVariables
from app.models.rules_config import BENEFITS_RULES_SPECIFICATION

class BusinessRuleEvaluator:
    @staticmethod
    def evaluate_operator(actual_value, operator: str, target_value) -> bool:
        """Executes basic predicate evaluations akin to a business-rules engine."""
        if operator == "equal_to":
            return actual_value == target_value
        if operator == "less_than_or_equal_to":
            return actual_value <= target_value
        if operator == "greater_than_or_equal_to":
            return actual_value >= target_value
        if operator == "less_than":
            return actual_value < target_value
        if operator == "greater_than":
            return actual_value > target_value
        return False

    @staticmethod
    def run(profile: UserProfile) -> list[BenefitEvaluation]:
        variables = RuleVariables(profile)
        evaluations = []

        for benefit_name, spec in BENEFITS_RULES_SPECIFICATION.items():
            criteria_results = []
            benefit_eligible = True

            for criterion in spec["criteria"]:
                actual_val = variables.get_value(criterion["variable"])
                op = criterion["operator"]
                target_val = criterion["value"]
                
                # Evaluate single condition
                status = BusinessRuleEvaluator.evaluate_operator(actual_val, op, target_val)
                
                if not status:
                    benefit_eligible = False

                criteria_results.append(CriterionResult(
                    criterion_name=criterion["name"],
                    status=status,
                    details=f"Condition: '{criterion['variable']}' {op} {target_val}. Valeur réelle: {actual_val}"
                ))

            # Dynamic Amount modulation logic if eligible
            estimated_amount = None
            if benefit_eligible and spec["calculate_amount"]:
                base = spec["base_amount"]
                if benefit_name == "Allocations Familiales":
                    children = variables.get_value("dependent_children_count")
                    resources = variables.get_value("household_total_resources")
                    computed = children * base
                    estimated_amount = computed * 0.25 if resources > 6000.0 else computed
                else:
                    estimated_amount = base

            evaluations.append(BenefitEvaluation(
                benefit_name=benefit_name,
                eligible=benefit_eligible,
                estimated_amount=estimated_amount,
                criteria_details=criteria_results
            ))

        return evaluations