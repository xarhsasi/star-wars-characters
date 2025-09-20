# Star Wars Api

## TLDR;
Run the bellow commands in order to run the project
```make up```
Sometimes the initial migration fails because it can't find the celery tables. I didn't have time to investigate it further.
So, just run:
```make up```
and you should be fine.

## CI/CD:
I did use github actions & workflows in order to automate the process with the testing and pre-commit hooks.

# Run the project
The project uses the
Star Wars API (FastAPI + SQLAlchemy async + Celery)

A production-ready FastAPI service that ingests Star Wars data from SWAPI, stores it in Postgres via SQLAlchemy 2.x (async), exposes typed REST endpoints, and runs background sync tasks with Celery.

Interactive docs live at /docs (Swagger) and /redoc.
FastAPI

#### ✨ Features
FastAPI app with JWT (Bearer) auth (OAuth2 password flow)
FastAPI

Async SQLAlchemy 2.x ORM + Alembic migrations

Celery worker for scheduled syncs from SWAPI (films, characters, starships)

Docker Compose dev stack (API, DB, Celery, broker)

Testing with pytest, async fixtures (anyio), and factory_boy

Lint/format with Ruff + pre-commit hooks
GitHub

#### 🧱 Tech stack

API: FastAPI, Uvicorn
FastAPI

DB/ORM: PostgreSQL (asyncpg), SQLAlchemy 2.x (AsyncSession), Alembic
SQLAlchemy Documentation

Background: Celery (Redis or RabbitMQ as broker)
Celery Documentation

Auth: OAuth2 Password + JWT (PyJWT/Passlib)
FastAPI

Lint/Format: Ruff + pre-commit
GitHub

Tests: pytest, anyio plugin
anyio.readthedocs.io

#### 🚀 Quickstart (Docker Compose)

Prereqs: Docker Desktop / Engine + Compose v2.
Docker Documentation

#### Database (async SQLAlchemy URL)
DATABASE_URL=postgresql+asyncpg://admin:admin@postgres:5432/star_wars_characters

Build & start

```make up```

## Run migrations

#### upgrade DB to latest
```make migrate```

#### Celery worker
docker compose run --rm worker celery -A src.celery_app worker -l info

#### Celery beat (if you schedule periodic tasks)
docker compose run --rm beat celery -A src.celery_app beat -l info


To run tasks inline during tests, enable eager mode (task_always_eager = True).

🧪 Running tests
#### unit + integration tests
make test

#### 🧹 Linting & formatting (pre-commit + Ruff)

Install pre-commit once:

pip install pre-commit
pre-commit install


Run on all files:

pre-commit run -a


Ruff is configured as a pre-commit hook (ruff-check, ruff-format) and can auto-fix common issues (including F401 unused imports) with --fix.
GitHub

#### 🔐 Authentication (JWT)

Create a new user via the Swagger UI
Authenticate against the recently created user to obtain a token.


Response:

`{"access_token": "...", "token_type": "bearer"}`

#### 🗄️ Database & Migrations
Async SQLAlchemy 2.x

Use one AsyncSession per request/task; don’t share the same session across concurrent asyncio tasks.
SQLAlchemy Documentation

Common Alembic commands
#### autogenerate a new revision
```make migrations message='{{message}}'```

#### upgrade to latest revision
```make migrate'```

#### ⛓️ Background sync (Celery)

Tasks (examples):

sync_films — fetch films from SWAPI and upsert into DB

sync_characters, sync_starships — same for other resources

sync_relationships — link films ⇄ characters/starships by URLs from SWAPI

Using uv:
#### install deps from requirements.txt
```make deps```
