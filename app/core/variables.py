from app.models.schemas import UserProfile

class RuleVariables:
    def __init__(self, profile: UserProfile):
        self.profile = profile

    def get_value(self, variable_name: str):
        # Direct attributes mapping
        if variable_name == "age":
            return self.profile.identity.age
        if variable_name == "is_detached_worker":
            return self.profile.identity.is_detached_worker
        if variable_name == "household_total_resources":
            return self.profile.income.household_total_resources
        
        # Computed Business Logic 1: Minimum months of residence per year (Required: >= 9)
        if variable_name == "has_stable_yearly_residence":
            return self.profile.identity.months_of_stable_residence >= 9 if hasattr(self.profile.identity, 'months_of_stable_residence') else self.profile.identity.months_in_france_per_year >= 9

        # Computed Business Logic 2: Nationality and Right to stay compliance
        if variable_name == "has_valid_administrative_status":
            zone = self.profile.identity.nationality_zone
            if zone == "FR":
                return True
            if zone == "UE":
                return self.profile.identity.has_stable_residence_right
            if zone == "OTHER":
                if not self.profile.identity.has_work_permitting_visa:
                    return False
                # Check exemptions for the 5-year residency rule
                if (self.profile.identity.years_of_regular_residence >= 5 or 
                    self.profile.identity.has_resident_card or 
                    self.profile.identity.is_refugee_or_protected or 
                    self.profile.identity.is_isolated_parent_with_child_under_3):
                    return True
                return False
            return False

        # Computed Business Logic 3: Minimum activity income based on specific status
        if variable_name == "passes_activity_income_threshold":
            status = self.profile.current_status
            income = self.profile.income.monthly_net_social_income
            
            # Specific student / apprentice / trainee threshold from your prompt
            if status in ["student", "apprentice", "trainee"]:
                return income >= 1117.26
            
            # Standard workers or partial unemployment must at least have some professional activity
            return income > 0.0

        raise ValueError(f"Variable '{variable_name}' is not defined in RuleVariables.")