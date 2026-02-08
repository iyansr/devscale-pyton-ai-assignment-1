dev:
	uv run uvicorn app.main:app --reload

db-migrate:
	uv run alembic revision --autogenerate -m "$(msg)"

db-upgrade:
	uv run alembic upgrade head
