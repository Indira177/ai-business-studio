from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database.database import Base, engine

from app.models.invoice import Invoice
from app.models.website import Website

from app.routers.invoice_router import router as invoice_router
from app.routers.website_router import router as website_router
from app.routers.website_list_router import router as website_list_router


# ==========================================
# DATABASE TABLES
# ==========================================

Base.metadata.create_all(
    bind=engine
)


# ==========================================
# APPLICATION
# ==========================================

app = FastAPI(
    title="AI Business Studio",
    description="AI-powered business automation platform",
    version="1.0.0"
)


# ==========================================
# INVOICE API
# ==========================================

app.include_router(
    invoice_router
)


# ==========================================
# WEBSITE BUILDER API
# ==========================================

app.include_router(
    website_router
)

app.include_router(
    website_list_router
)


# ==========================================
# STATIC FILES
# ==========================================

app.mount(
    "/static",
    StaticFiles(
        directory="app/static"
    ),
    name="static"
)


# ==========================================
# DASHBOARD
# ==========================================

@app.get("/")
def dashboard():

    return FileResponse(
        "app/static/index.html"
    )


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/api/health")
def health_check():

    return {
        "application": "AI Business Studio",
        "status": "UP"
    }