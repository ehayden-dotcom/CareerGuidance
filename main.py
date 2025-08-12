"""FastAPI application entrypoint.

This module initialises the FastAPI app, applies CORS middleware and
registers the API routers.  During startup it creates the database
tables and seeds the careers table from the JSON data file when the
`SEED_DATA` environment variable is set to a truthy value.
"""
import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import health, careers, recommend
from .models import create_db_and_tables, seed_db_if_needed

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="AI Career Pathways Advisor", version="0.1.0")

    # Allow CORS for the frontend; defaults to localhost:5173 but can be overridden
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in allowed_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup() -> None:
        """Create tables and seed database on startup."""
        create_db_and_tables()
        # Only seed when explicitly requested
        seed_flag = os.getenv("SEED_DATA", "false").lower() in {"1", "true", "yes"}
        if seed_flag:
            seed_db_if_needed()

    # Include routers under /api prefix
    app.include_router(health.router, prefix="/api")
    app.include_router(careers.router, prefix="/api")
    app.include_router(recommend.router, prefix="/api")

    return app


app = create_app()