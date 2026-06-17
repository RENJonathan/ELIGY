from fastapi import APIRouter, status, HTTPException
from app.models.schemas import UserProfile, EngineResponse
from app.core.engine import BusinessRuleEvaluator

# Initialize the router for the evaluation endpoints
router = APIRouter(
    prefix="/evaluate",
    tags=["Eligibility Engine"]
)

@router.post(
    "",
    response_model=EngineResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluate user eligibility for social benefits",
    description="Accepts a structured JSON user profile, executes compliance rules, and returns detailed criteria status."
)
def evaluate_eligibility(profile: UserProfile):
    try:
        # Pass the validated Pydantic profile to the business rules core execution layer
        evaluations = BusinessRuleEvaluator.run(profile)
        return EngineResponse(user_eligible_benefits=evaluations)
    except ValueError as val_err:
        # Handle cases where profile mapping fails due to unmapped/invalid variables
        raise HTTPException(
            status_code=status.HTTP_420_METHOD_FAILURE,
            detail=f"Rule engine variable processing error: {str(val_err)}"
        )
    except Exception as err:
        # Generic fallback for internal unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred within the rule core: {str(err)}"
        )