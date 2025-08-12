"""Dependency providers for FastAPI routes.

This module defines reusable dependency functions that can be injected
into route handlers.  Currently it exposes a database session provider.
"""
from .models import get_session

__all__ = ["get_session"]