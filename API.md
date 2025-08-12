# API Reference

All endpoints are served under the `/api` prefix.  Responses are JSON encoded and follow standard HTTP status semantics.  Below is a summary of the available endpoints.

## GET `/api/health`

Returns a simple status object that can be used by load balancers or uptime monitoring tools to confirm that the API is running.

### Response

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "ok"
}
```

## GET `/api/careers`

Retrieves the full list of careers stored in the database.  Each career object corresponds to an entry in `data/careers.json` and includes its identifier, name, cluster, required skills, suggested subjects, VET options, pathways and job outlook.

### Response

```
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "careerId": "CR001",
    "name": "Paramedic",
    "cluster": "Health",
    "requiredSkills": ["Empathy", "Communication", "Problem-Solving"],
    "suggestedSubjects": ["Biology", "Chemistry", "Physical Education"],
    "vetOptions": ["Certificate IV in Health Care"],
    "pathways": ["Bachelor of Paramedicine"],
    "jobOutlook": "Strong demand"
  },
  ...
]
```

## GET `/api/careers/{careerId}`

Retrieves a single career by its `careerId`.  If the career is not found, the endpoint returns a `404` response.

### Parameters

| Name      | Type   | Description                   |
|-----------|--------|-------------------------------|
| `careerId` | string | The identifier of the career. |

### Response

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "careerId": "CR001",
  "name": "Paramedic",
  "cluster": "Health",
  ...
}
```

If the career does not exist:

```
HTTP/1.1 404 Not Found
{
  "detail": "Career not found"
}
```

## POST `/api/recommend`

Accepts a student profile and returns an array of three recommended careers ranked by confidence.  The scoring algorithm is deterministic and based on overlap of the student's interests and strengths with each career, modified by academic performance.  See `docs/MATCHING.md` for details.

### Request Body

The body must be JSON and match the following schema:

| Field               | Type                 | Description                                                      |
|---------------------|----------------------|------------------------------------------------------------------|
| `name`              | string               | Student’s name.                                                  |
| `yearLevel`         | integer              | School year level (e.g. 7–12).                                   |
| `interests`         | array of strings     | List of interests selected from the canonical interests.         |
| `strengths`         | array of strings     | List of strengths selected from the canonical strengths.         |
| `academicPerformance` | string (`High`, `Medium`, `Low`) | Self‑reported academic performance.                  |

### Response

Returns a list of three recommendation objects sorted by decreasing confidence.

Each recommendation has the following structure:

| Field             | Type             | Description                                                          |
|-------------------|------------------|----------------------------------------------------------------------|
| `careerId`        | string           | The identifier of the recommended career.                            |
| `name`            | string           | Career name.                                                         |
| `cluster`         | string           | The cluster/category of the career.                                  |
| `confidence`      | float            | A score between `0` and `1` representing the relative suitability.   |
| `why`             | string           | A human‑readable explanation of the match (interests and strengths). |
| `suggestedSubjects` | array of strings | Recommended school subjects for this career.                         |
| `vetOptions`      | array of strings | VET or certificate options associated with the career.               |
| `nextSteps`       | string           | A short summary of actions the student can take to pursue this path. |

### Example

Request:

```bash
curl -X POST http://localhost/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sam",
    "yearLevel": 10,
    "interests": ["IT", "STEM"],
    "strengths": ["Problem-Solving", "Technical Skills"],
    "academicPerformance": "High"
  }'
```

Response:

```
[
  {
    "careerId": "CR002",
    "name": "Software Developer",
    "cluster": "IT",
    "confidence": 0.83,
    "why": "Matches your interests (IT, STEM) and strengths (Problem-Solving, Technical Skills)",
    "suggestedSubjects": ["Mathematics", "Computer Science", "Design"],
    "vetOptions": ["Diploma of Information Technology"],
    "nextSteps": "Consider focusing on Mathematics, Computer Science and Design and exploring pathways: Bachelor of Computer Science, Bachelor of Software Engineering."
  },
  ... two more items ...
]
```