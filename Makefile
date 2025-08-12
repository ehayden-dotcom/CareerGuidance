.PHONY: dev test build up down fmt lint seed

# Run the backend in dev mode (autoreload)
dev:
	uvicorn backend.app.main:app --app-dir backend/app --reload --port $(BACKEND_PORT)

# Run backend and frontend tests
test:
	(cd backend && pytest)
	(cd frontend && npm test -- --run)

# Build Docker images via compose
build:
	docker compose build

# Bring up the stack in the background
up:
	docker compose up -d

# Tear down the stack
down:
	docker compose down

# Format backend and frontend code
fmt:
	black backend
	ruff backend --fix
	prettier -w frontend

# Lint backend and frontend code without fixing
lint:
	ruff backend
	eslint frontend

# Seed the database with data/careers.json
seed:
	SEED_DATA=true python -m backend.app.main