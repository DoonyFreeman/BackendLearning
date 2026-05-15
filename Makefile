.PHONY: dev test lint migrate seed docker-up docker-down

dev:
	uvicorn src.main:app --reload --host 0.0.0.0

test:
	pytest -v --tb=short

lint:
	ruff check src/ tests/

migrate:
	alembic upgrade head

migrate-new:
	alembic revision --autogenerate -m "$(name)"

seed:
	python seed_data.py

docker-up:
	docker compose up

docker-down:
	docker compose down

docker-rebuild:
	docker compose down && docker compose up --build
