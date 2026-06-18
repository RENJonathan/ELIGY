from pydantic import BaseModel, Field
from typing import Optional, List

class IdentityProfile(BaseModel):
    age: int = Field(..., ge=0)
    country_of_residence: str = Field(default="FR")
    nationality_zone: str = Field(..., description="FR / UE_EEE_CH / OTHER")
    months_in_france_per_year: int = Field(..., ge=0, le=12)
    months_of_stable_residence: int = Field(..., ge=0)
    is_detached_worker: bool = Field(...)
    has_stable_residence_right: bool = Field(...)
    has_work_permitting_visa: bool = Field(...)
    years_of_regular_residence: int = Field(..., ge=0)
    has_resident_card: bool = Field(...)
    is_refugee_or_protected: bool = Field(...)
    is_stateless: bool = Field(default=False)
    is_isolated_parent_with_child_under_3: bool = Field(...)

class IncomeProfile(BaseModel):
    monthly_net_social_income: float = Field(..., ge=0)
    household_total_resources: float = Field(..., ge=0)

class FamilyProfile(BaseModel):
    dependent_children_count: int = Field(..., ge=0)
    children_max_age: int = Field(default=0, description="Age of the oldest dependent child")

class UserProfile(BaseModel):
    identity: IdentityProfile
    income: IncomeProfile
    family: FamilyProfile
    current_status: str = Field(..., description="employee / self_employed / partial_unemployment / technical_unemployment / student / other")

class CriterionResult(BaseModel):
    criterion_name: str
    status: bool
    details: str

class BenefitEvaluation(BaseModel):
    benefit_name: str
    eligible: bool
    estimated_amount: Optional[float] = None
    criteria_details: List[CriterionResult]

class EngineResponse(BaseModel):
    user_eligible_benefits: List[BenefitEvaluation]