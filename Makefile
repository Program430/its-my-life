.PHONY: up down run test lint format

up:
	docker compose up -d

down:
	docker compose down

run:
	poetry run uvicorn src.main:app --reload

test:
	poetry run pytest

lint:
	poetry run ruff check .

fix:
	poetry run ruff check --fix . && poetry run ruff format .

db-revision:
	poetry run alembic revision --autogenerate -m "$(msg)"

db-migrate:
	poetry run alembic upgrade head

db-rollback:
	poetry run alembic downgrade -1
