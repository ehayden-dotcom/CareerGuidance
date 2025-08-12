"""Career endpoints.

Expose REST endpoints to list all careers and retrieve a single career by
its identifier.  These endpoints query the SQLite database via the
SQLModel session dependency.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..models import Career
from ..deps import get_session

router = APIRouter()


@router.get("/careers", response_model=list[Career])
def list_careers(session: Session = Depends(get_session)) -> list[Career]:
    """Return all careers in the database."""
    result = session.exec(select(Career))
    return result.all()


@router.get("/careers/{career_id}", response_model=Career)
def get_career(career_id: str, session: Session = Depends(get_session)) -> Career:
    """Return a single career by its `careerId`.  Raises 404 if not found."""
    statement = select(Career).where(Career.careerId == career_id)
    career = session.exec(statement).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")
    return career