SOURCE_DIR = ./star_wars_characters


help:
	clear;
	@echo "=============================== Usage ==============================="
	@echo "make build       - Build the project"

uv-requirements:
	uv export -o requirements.txt

migrations: # Create alembic migrations
	docker compose run fastapi alembic revision --autogenerate -m ${message}

shell-plus: # Ipython shell with a lot of stuff loaded
	docker compose run ${exec_args} --rm fastapi python /app/src/shell_plus.py
