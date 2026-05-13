from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import health, orders

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url="/openapi.json"
)

# Set up CORS
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(orders.router, prefix="/v1/orders", tags=["orders"])

@app.get("/")
def root():
    return {"message": "Welcome to Khafeefa API"}
