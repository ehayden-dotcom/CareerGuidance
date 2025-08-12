"""Rule‑based career matching engine.

This module implements a simple deterministic scoring algorithm for
matching student profiles to careers.  It measures the overlap of
interests and strengths using configurable weights and applies a small
bonus or penalty based on academic performance.  The engine returns
the top three careers along with confidence scores and rationale
strings.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from ..schemas import Recommendation, StudentProfile
from ..models import Career

# Weight constants – adjust these values to tweak the scoring algorithm
INTEREST_WEIGHT: float = 0.6
STRENGTH_WEIGHT: float = 0.3
PERFORMANCE_BOOST: float = 0.1  # for High performance
PERFORMANCE_PENALTY: float = 0.1  # for Low performance


def _performance_modifier(performance: str) -> float:
    """Return a modifier based on academic performance."""
    perf = performance.lower()
    if perf == "high":
        return PERFORMANCE_BOOST
    if perf == "low":
        return -PERFORMANCE_PENALTY
    return 0.0


def match_careers(student: StudentProfile, careers: Sequence[Career]) -> List[Recommendation]:
    """Compute scores for all careers and return the top three recommendations.

    Args:
        student: The student's profile containing name, year level, interests,
            strengths and academic performance.
        careers: A sequence of careers loaded from the database.

    Returns:
        A list of three `Recommendation` objects sorted by descending confidence.
    """
    results: List[tuple[float, Career, List[str], List[str]]] = []
    for career in careers:
        # Compute interest overlap: a career's cluster counts as a single interest tag
        interest_overlap = 1 if career.cluster in student.interests else 0
        matched_interests = [career.cluster] if interest_overlap else []
        # Compute strengths overlap: count how many of the student's strengths appear in the career's required skills
        matched_strengths = [s for s in student.strengths if s in career.requiredSkills]

        interests_score = (interest_overlap / max(1, len(student.interests))) * INTEREST_WEIGHT
        strengths_score = (len(matched_strengths) / max(1, len(student.strengths))) * STRENGTH_WEIGHT
        base_score = interests_score + strengths_score

        raw_score = base_score + _performance_modifier(student.academicPerformance)
        confidence = max(0.0, min(1.0, raw_score))

        results.append((confidence, career, matched_interests, matched_strengths))

    # Sort by confidence descending then by career name for consistency
    results.sort(key=lambda x: (-x[0], x[1].name))
    top_three = results[:3]

    recommendations: List[Recommendation] = []
    for score, career, mi, ms in top_three:
        # Build rationale string
        interest_part = f"interests ({', '.join(mi)})" if mi else "no matching interests"
        strength_part = f"strengths ({', '.join(ms)})" if ms else "no matching strengths"
        why = f"Matches your {interest_part} and {strength_part}"

        # Construct next steps: highlight subjects and pathways
        next_steps = (
            f"Consider focusing on subjects {', '.join(career.suggestedSubjects)} and exploring pathways: "
            f"{', '.join(career.pathways)}."
        )

        recommendations.append(
            Recommendation(
                careerId=career.careerId,
                name=career.name,
                cluster=career.cluster,
                confidence=round(score, 2),
                why=why,
                suggestedSubjects=career.suggestedSubjects,
                vetOptions=career.vetOptions,
                nextSteps=next_steps,
            )
        )

    return recommendations