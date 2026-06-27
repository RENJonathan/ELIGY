from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.evaluate import router as evaluate_router_v1

app = FastAPI(
    title="ZIZOFA-ALLOCS - Dynamic Business Rules Engine",
    description="Decoupled backend rule engine driven by dictionary configurations.",
    version="2.0.0"
)

# Allow the local Vite application to call the API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the sub-routers with their respective API version prefixes
app.include_router(evaluate_router_v1, prefix="/api/v1")

@app.get("/health", status_code=status.HTTP_200_OK, tags=["System"])
def health_check():
    return {"status": "healthy", "engine": "business-rules-driven"}
