"""Pydantic schemas for request and response bodies.

These classes define the shape of data exchanged between the client and
the server.  They are separate from the SQLModel models so that the
external API surface can evolve independently of the database schema.
"""
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class StudentProfile(BaseModel):
    """Represents the student's input when requesting recommendations."""

    name: str = Field(..., description="Student's full name")
    yearLevel: int = Field(..., ge=1, description="School year level (1–12)")
    interests: List[str] = Field(..., description="List of selected interests")
    strengths: List[str] = Field(..., description="List of selected strengths")
    academicPerformance: Literal["High", "Medium", "Low"] = Field(
        ..., description="Self‑reported academic performance"
    )


class Recommendation(BaseModel):
    """Represents a single career recommendation returned to the client."""

    careerId: str
    name: str
    cluster: str
    confidence: float
    why: str
    suggestedSubjects: List[str]
    vetOptions: List[str]
    nextSteps: str