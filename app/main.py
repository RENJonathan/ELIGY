from fastapi import FastAPI, status
from app.api.v1.evaluate import router as evaluate_router_v1

app = FastAPI(
    title="ZIZOFA-ALLOCS - Dynamic Business Rules Engine",
    description="Decoupled backend rule engine driven by dictionary configurations.",
    version="2.0.0"
)

# Register the sub-routers with their respective API version prefixes
app.include_router(evaluate_router_v1, prefix="/api/v1")

@app.get("/health", status_code=status.HTTP_200_OK, tags=["System"])
def health_check():
    return {"status": "healthy", "engine": "business-rules-driven"}