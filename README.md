# AI Career Pathways Advisor

The **AI Career Pathways Advisor** is a full‑stack web application that helps secondary school students explore potential careers based on their interests, strengths and academic performance.  A simple, rule‑based matching engine recommends the top three careers from a curated data set and explains why each career is a good fit.  While a hook for an LLM is provided, the application works end‑to‑end without any external APIs.

## Features

- **Transparent Matching** – A deterministic scoring engine matches student profiles to careers using weighted overlaps of interests and strengths and adjusts scores based on academic performance.
- **Curated Career Data** – A JSON data set of 15–25 careers with clusters, required skills, suggested subjects, VET options and pathways is bundled with the app.
- **RESTful API** – A FastAPI backend serves health checks, career listings, and recommendations.  The API is fully documented under `docs/API.md`.
- **Responsive Frontend** – A React + TypeScript frontend built with Vite and TailwindCSS provides a simple form for entering a student profile and displays ranked recommendations.
- **Dockerised Deployment** – A `docker-compose.yml` brings up the backend, frontend and an nginx reverse proxy in one command.  A Makefile simplifies common tasks like running the dev server, running tests and formatting code.
- **CI/CD** – GitHub Actions lint, test and build the project on pull requests and push to `main`.  A separate workflow deploys the built frontend to GitHub Pages.

## Quickstart

### Prerequisites

- [Docker Compose](https://docs.docker.com/compose/install/) and Docker installed on your system.
- [Node.js](https://nodejs.org/) (only required for local frontend development, not when using Docker).

### Running with Docker

Start the entire stack (backend, frontend and nginx) with one command:

```bash
docker compose up -d
```

This will build the images if necessary and serve the application at `http://localhost`.  The frontend will attempt to access the backend via `/api`; if the backend is unreachable, it shows an appropriate message.

### Running in Development

If you prefer to run the services separately during development:

```bash
# backend
make dev     # runs `uvicorn` with auto‑reload on port 8000

# frontend
cd frontend
npm install
npm run dev  # serves the React app on port 5173

# database seed (optional)
make seed    # reseeds the database from data/careers.json
```

### Running Tests

Run the backend and frontend tests together via the Makefile:

```bash
make test
```

This command runs `pytest` for the backend and `vitest` for the frontend.  Both suites must pass for CI to succeed.

## Project Structure

The repository is organised as follows:

```
ai-career-pathways-advisor/
├─ README.md                  # This file
├─ LICENSE                    # MIT license
├─ CODE_OF_CONDUCT.md         # Contributor Covenant
├─ CONTRIBUTING.md            # How to contribute
├─ .gitignore
├─ .env.example               # Example environment variables
├─ Makefile                   # Developer shortcuts
├─ docker-compose.yml         # Compose definition
├─ .github/                   # CI/CD workflows
│  ├─ workflows/
│  │  ├─ ci.yml               # Linting, tests and builds
│  │  └─ deploy-pages.yml     # Deploys frontend to GitHub Pages
├─ data/
│  ├─ clusters.json           # Canonical interest/strength tags
│  ├─ careers.json            # Career data set
│  └─ sample_students.json    # Example profiles for the UI
├─ docs/
│  ├─ API.md                  # REST API specification
│  ├─ MATCHING.md             # Matching algorithm documentation
│  └─ PROMPTS.md              # LLM prompt template
├─ backend/
│  ├─ requirements.txt        # Python dependencies
│  ├─ app/
│  │  ├─ main.py              # FastAPI application
│  │  ├─ models.py            # SQLModel definitions and DB helpers
│  │  ├─ schemas.py           # Pydantic models
│  │  ├─ deps.py              # Dependency overrides
│  │  ├─ matching/
│  │  │  ├─ engine.py         # Matching engine
│  │  │  └─ prompts.py        # Prompt template for LLM hook
│  │  └─ routers/
│  │     ├─ health.py         # /api/health endpoint
│  │     ├─ careers.py        # /api/careers endpoints
│  │     └─ recommend.py      # /api/recommend endpoint
│  └─ tests/
│     ├─ test_health.py
│     ├─ test_careers.py
│     └─ test_recommend.py
├─ frontend/
│  ├─ index.html              # Vite entry point
│  ├─ package.json
│  ├─ tsconfig.json
│  ├─ vite.config.ts
│  ├─ postcss.config.js
│  ├─ tailwind.config.js
│  ├─ src/
│  │  ├─ main.tsx
│  │  ├─ App.tsx
│  │  ├─ components/
│  │  │  ├─ StudentForm.tsx
│  │  │  └─ Recommendations.tsx
│  │  ├─ lib/api.ts
│  │  └─ types.ts
│  └─ tests/
│     └─ App.test.tsx
└─ ops/
   ├─ Dockerfile.backend
   ├─ Dockerfile.frontend
   └─ nginx.conf
```

## Roadmap

Future iterations might include:

- Pluggable machine learning or LLM modules to provide personalised rationale beyond simple overlap metrics.
- User accounts and persistence of student sessions.
- Administration interfaces to manage the career data set.
- Integration with external datasets such as labour market outlooks.

## Screenshots

Screenshots of the working application can be added here after running the stack locally.  When you run `docker compose up -d` and visit the application in your browser, take screenshots of the form and the recommendations page and place them in this section.
