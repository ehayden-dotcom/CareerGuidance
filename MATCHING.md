# Matching Algorithm

The matching engine in this project is deliberately simple and transparent.  It assigns a score to every career based on how well a student’s interests and strengths align with the canonical tags defined in `data/clusters.json`.  The top three careers with the highest scores are returned to the client along with a confidence score and rationale.

## Scoring Formula

For each career and student profile we compute:

```
interest_matches  = number of overlapping interests between student and career cluster
strength_matches  = number of overlapping strengths between student and career requiredSkills

interests_score   = (interest_matches / max(1, len(student.interests))) * INTEREST_WEIGHT
strengths_score   = (strength_matches / max(1, len(student.strengths))) * STRENGTH_WEIGHT

base_score        = interests_score + strengths_score

performance_mod   = +PERFORMANCE_BOOST if academicPerformance == 'High'
                  =  0               if academicPerformance == 'Medium'
                  = -PERFORMANCE_PENALTY if academicPerformance == 'Low'

raw_score         = base_score + performance_mod

confidence        = clamp(raw_score, 0.0, 1.0)
```

By default the weights are:

| Parameter             | Value | Description                                  |
|-----------------------|-------|----------------------------------------------|
| `INTEREST_WEIGHT`     | 0.6   | Weight applied to interest overlaps          |
| `STRENGTH_WEIGHT`     | 0.3   | Weight applied to strengths overlaps         |
| `PERFORMANCE_BOOST`   | 0.1   | Added to score for students with high performance |
| `PERFORMANCE_PENALTY` | 0.1   | Subtracted from score for students with low performance |

These constants are defined in `backend/app/matching/engine.py` and can be adjusted there.  Feel free to experiment with different values; just ensure the final score remains within the range `[0,1]`.

## Rationale

The rationale returned with each recommendation lists the specific interests and strengths that overlapped between the student and career.  This makes the recommendations easy to understand and gives students clear insight into why a career was suggested.

## Extending the Engine

While the current engine is deterministic and transparent, it is designed to be extended.  You could for example:

- Incorporate academic grades for specific subjects into the scoring.
- Use machine learning to learn weights from historical data.
- Add a hook to call a Large Language Model (LLM) to generate richer explanations or alternative career suggestions.  See `docs/PROMPTS.md` for the prompt template used by the optional LLM hook.