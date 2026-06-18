from app.models.schemas import UserProfile

class RuleVariables:
    """Translates the structured JSON profile into a flat dictionary matching the config keys."""
    
    @staticmethod
    def extract(profile: UserProfile) -> dict:
        # Pre-computing specific limits needed by the AME rules
        ame_threshold_passed = profile.income.household_total_resources <= 810.0
        
        # Valid activity types as defined in PA_8
        valid_activities = ["employee", "self_employed", "partial_unemployment", "technical_unemployment"]

        return {
            "age_min": profile.identity.age,
            "min_months_residence_per_year": profile.identity.months_in_france_per_year,
            "country_of_residence": profile.identity.country_of_residence,
            "detached_worker": profile.identity.is_detached_worker,
            "nationality_zone": profile.identity.nationality_zone,
            "right_to_stay": profile.identity.has_stable_residence_right,
            "has_valid_residence_permit": profile.identity.has_work_permitting_visa,
            "permit_authorizes_work": profile.identity.has_work_permitting_visa,
            "years_of_residence_in_france_min": profile.identity.years_of_regular_residence,
            "has_resident_card": profile.identity.has_resident_card,
            "status_refugee": profile.identity.is_refugee_or_protected,
            "status_subsidiary_protection": profile.identity.is_refugee_or_protected,
            "status_stateless": profile.identity.is_stateless,
            "single_parent_with_child_under_3": profile.identity.is_isolated_parent_with_child_under_3,
            "employment_required": profile.current_status in valid_activities,
            "activity_type_allowed": profile.current_status,
            "student_status": profile.current_status == "student",
            "monthly_net_income_min": profile.income.monthly_net_social_income,
            "min_months_residence": profile.identity.months_of_stable_residence,
            "eligible_to_health_insurance": profile.identity.has_stable_residence_right, 
            "household_income_under_threshold": ame_threshold_passed,
            "children_count_min": profile.family.dependent_children_count,
            "children_all_under_age": profile.family.children_max_age,
            "residence_stable": profile.identity.months_in_france_per_year >= 9,
            "income_affects_amount": True
        }