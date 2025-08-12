"""Health check endpoint.

Provides a simple endpoint for checking whether the service is running.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return a simple OK status for health monitoring."""
    return {"status": "ok"}