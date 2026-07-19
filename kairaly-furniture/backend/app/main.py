import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import admin_products, auth, branches, products
from app.config import settings
from app.database import Base, engine

# Create tables automatically in dev (use Alembic migrations in production).
Base.metadata.create_all(bind=engine)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title=settings.APP_NAME,
    description="REST API for the Kairaly Furniture sofa catalog (MVP).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded product images.
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(branches.router, prefix=settings.API_V1_PREFIX)
app.include_router(products.router, prefix=settings.API_V1_PREFIX)
app.include_router(admin_products.router, prefix=settings.API_V1_PREFIX)
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Health"], summary="Health check")
def root():
    return {
        "app": settings.APP_NAME,
        "status": "ok",
        "docs": "/docs",
    }
