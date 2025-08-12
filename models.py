"""Database models and helpers using SQLModel.

This module defines the `Career` table, manages the database engine and
provides convenience functions for creating tables and seeding data from
the JSON files in the repository's data directory.
"""
import json
import os
from pathlib import Path
from typing import Iterator, List, Optional

from sqlmodel import SQLModel, Field, Session, create_engine, select, Column, JSON

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(DATABASE_URL, echo=False)


class Career(SQLModel, table=True):
    """Represents a career in the database.

    The integer `id` is an auto‑incrementing primary key.  The
    `careerId` field stores a stable identifier imported from the JSON
    data and is indexed to allow lookup via the API.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    careerId: str = Field(index=True)
    name: str
    cluster: str
    requiredSkills: List[str] = Field(sa_column=Column(JSON))
    suggestedSubjects: List[str] = Field(sa_column=Column(JSON))
    vetOptions: List[str] = Field(sa_column=Column(JSON))
    pathways: List[str] = Field(sa_column=Column(JSON))
    jobOutlook: str


def create_db_and_tables() -> None:
    """Create database tables if they do not already exist."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """Provide a database session for dependency injection."""
    with Session(engine) as session:
        yield session


def _load_careers_json() -> List[dict]:
    """Load the careers data from the JSON file in the repository.

    The JSON file is located at `data/careers.json` relative to the
    project root.  When running via Docker compose the volume mount
    ensures that `./data` is available in the working directory.
    """
    # Determine the base directory (two levels above this file)
    base_dir = Path(__file__).resolve().parents[2]
    data_file = base_dir / "data" / "careers.json"
    with data_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def seed_db_if_needed() -> None:
    """Seed the careers table with data from the JSON file.

    This function checks whether any careers exist in the database.  If
    not, it inserts all records from the JSON file.  It is idempotent and
    will not create duplicates if called multiple times.
    """
    careers_data = _load_careers_json()
    with Session(engine) as session:
        result = session.exec(select(Career))
        existing_count = len(result.all())
        if existing_count == 0:
            # Only seed when table is empty
            career_objects = [Career(**career) for career in careers_data]
            session.add_all(career_objects)
            session.commit()