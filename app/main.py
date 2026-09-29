import os
from pathlib import Path

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from .routes import router


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description="AI-powered personalized fitness planning application",
    version="1.0.0"
)


# ============================================================
# SESSION MIDDLEWARE
# ============================================================

SESSION_SECRET_KEY = os.getenv(
    "SESSION_SECRET_KEY"
)

if not SESSION_SECRET_KEY:
    raise RuntimeError(
        "SESSION_SECRET_KEY is missing from .env"
    )


app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# ============================================================
# JINJA2 TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)

app.state.templates = templates


# ============================================================
# ROUTES
# ============================================================

app.include_router(router)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health_check():

    return {
        "status": "ok",
        "application": "FitBuddy"
    }