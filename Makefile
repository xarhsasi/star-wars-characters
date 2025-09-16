SOURCE_DIR = ./star_wars_characters


help:
	clear;
	@echo "=============================== Usage ==============================="
	@echo "make uv-requirements - Export requirements.txt from Pipfile"
	@echo "make migrations message='message' - Create alembic migrations"
	@echo "make shell-plus - Ipython shell with a lot of stuff loaded"
	@echo "make deps - Install dependencies from uv-requirements.txt and uv sync"
	@echo "make test - Run tests"
	@echo "make build - Build docker images"
	@echo "make up - Run docker compose"
	@echo "======================================================================"


uv-requirements:
	uv export --format requirements-txt --no-emit-project -o requirements.txt

migrations: # Create alembic migrations
	docker compose run fastapi alembic revision --autogenerate -m ${message}

shell-plus: # Ipython shell with a lot of stuff loaded
	docker compose run --rm fastapi python /app/src/shell_plus.py

deps:
	pip install -r uv-requirements.txt
	uv sync

test: # Run tests
	docker compose run --rm fastapi pytest -vv

build:
	docker compose build

up:
	docker compose up
