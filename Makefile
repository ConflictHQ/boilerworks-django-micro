.PHONY: up down build logs shell migrate migrations test lint check ps

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up -d --build

logs:
	docker compose logs -f api

shell:
	docker compose exec api bash

migrate:
	docker compose exec api python manage.py migrate

migrations:
	docker compose exec api python manage.py makemigrations $(app)

test:
	docker compose exec api python -m pytest --cov --cov-report=term-missing -v

lint:
	docker compose exec api python -m ruff check . && docker compose exec api python -m ruff format --check .

check: lint test

ps:
	docker compose ps

local-test:
	uv run python -m pytest --cov --cov-report=term-missing -v

local-lint:
	uv run ruff check . && uv run ruff format --check .
