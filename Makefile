dev:
	uv run uvicorn app.main:app --reload

db-migrate:
	uv run alembic revision --autogenerate -m "$(msg)"

db-upgrade:
	uv run alembic upgrade head

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix .

format:
	uv run ruff format .
