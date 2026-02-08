# Dota2 Tools API

A RESTful API built with FastAPI for managing Dota 2 heroes and players. This application allows you to create, read, update, and delete heroes and players, as well as manage player favorite heroes relationships.

## Features

- **Hero Management**: Create, read, update, and delete Dota 2 heroes with attributes like name, type, and difficulty
- **Player Management**: Manage players with username and rank information
- **Favorite Heroes**: Players can have multiple favorite heroes (many-to-many relationship)
- **Pagination**: All list endpoints support pagination with configurable page size
- **Auto-generated IDs**: Uses CUID2 for unique identifier generation
- **Interactive API Documentation**: Scalar API reference available for easy testing
- **Database Migrations**: Alembic integration for database schema versioning

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: SQLite
- **Migration Tool**: Alembic
- **Package Manager**: uv
- **Server**: Uvicorn

## Project Structure

```
.
├── app/
│   ├── core/           # Core configurations and schemas
│   ├── models/         # Database models and engine
│   ├── modules/        # API routes and serializers
│   │   ├── heroes/     # Heroes module
│   │   └── players/    # Players module
│   └── utils/          # Utility functions
├── alembic/            # Database migration files
├── alembic.ini         # Alembic configuration
├── pyproject.toml      # Project dependencies
├── uv.lock            # Lock file for dependencies
└── dota2.db           # SQLite database file
```

## Configuration

The application uses environment-based configuration through `app/core/settings.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | "Dota2 Tools" | Application name |
| `VERSION` | "0.0.1" | API version |

Database configuration is located in `app/models/engine.py`:
- Default database: SQLite (`sqlite:///./dota2.db`)

## Installation & Setup

### Prerequisites

- Python >= 3.14.2
- [uv](https://docs.astral.sh/uv/) package manager

### Install Dependencies

```bash
uv sync
```

### Run Database Migrations

```bash
make db-upgrade
# or
uv run alembic upgrade head
```

## Running the Application

### Development Mode (with auto-reload)

```bash
make dev
# or
uv run uvicorn app.main:app --reload
```

The API will be available at:
- API Base: `http://localhost:8000/api`
- Scalar Documentation: `http://localhost:8000/scalar`

## API Routes

### Heroes

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `GET` | `/api/heroes/` | List all heroes (paginated) | 200 OK |
| `GET` | `/api/heroes/{hero_id}` | Get a specific hero by ID | 200 OK, 404 Not Found |
| `POST` | `/api/heroes/` | Create a new hero | 201 Created |
| `PATCH` | `/api/heroes/{hero_id}` | Update an existing hero | 200 OK, 404 Not Found |
| `DELETE` | `/api/heroes/{hero_id}` | Delete a hero | 200 OK, 404 Not Found |

**Query Parameters for List:**
- `page` (int, default: 1): Page number
- `per_page` (int, default: 10): Items per page

**Request Body (Create/Update):**
```json
{
  "name": "Anti-Mage",
  "type": "Agility",
  "difficulty": "Medium"
}
```

### Players

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `GET` | `/api/players/` | List all players (paginated) | 200 OK |
| `GET` | `/api/players/{player_id}` | Get a specific player by ID | 200 OK, 404 Not Found |
| `POST` | `/api/players/` | Create a new player | 201 Created |
| `PATCH` | `/api/players/{player_id}` | Update an existing player | 200 OK, 404 Not Found |
| `DELETE` | `/api/players/{player_id}` | Delete a player | 200 OK, 404 Not Found |

**Query Parameters for List:**
- `page` (int, default: 1): Page number
- `per_page` (int, default: 10): Items per page

**Request Body (Create):**
```json
{
  "username": "player123",
  "rank": "Immortal"
}
```

**Request Body (Update):**
```json
{
  "username": "new_username",
  "rank": "Divine"
}
```

### Player Favorite Heroes

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/api/players/{player_id}/favourite-heroes` | Add a hero to player's favorites | 200 OK, 404 Not Found, 409 Conflict |

**Request Body:**
```json
{
  "hero_id": "cl..."
}
```

## Response Format

### Single Resource Response

```json
{
  "data": {
    "id": "cl...",
    "name": "Anti-Mage",
    "type": "Agility",
    "difficulty": "Medium"
  }
}
```

### Paginated List Response

```json
{
  "message": "Heroes retrieved successfully",
  "data": [...],
  "pagination": {
    "current_page": 1,
    "total_records": 50,
    "total_pages": 5
  }
}
```

## Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| `200` | OK | Successful GET, PATCH, DELETE requests |
| `201` | Created | Successful POST requests |
| `404` | Not Found | Resource not found (hero/player doesn't exist) |
| `409` | Conflict | Duplicate entry (hero already in favorites) |
| `422` | Unprocessable Entity | Validation error (invalid request body) |

## Database Migrations

### Create a New Migration

```bash
make db-migrate msg="add_new_table"
# or
uv run alembic revision --autogenerate -m "add_new_table"
```

### Apply Migrations

```bash
make db-upgrade
# or
uv run alembic upgrade head
```

### Downgrade Migrations

```bash
uv run alembic downgrade -1
```

## Data Models

### Hero

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (CUID) | Primary key, auto-generated |
| `name` | string | Hero name |
| `type` | string | Hero type (e.g., Strength, Agility, Intelligence) |
| `difficulty` | string | Difficulty level |

### Player

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (CUID) | Primary key, auto-generated |
| `username` | string | Player's username |
| `rank` | string | Player's rank (e.g., Herald, Guardian, Crusader, etc.) |
| `favourite_heroes` | list[Hero] | Many-to-many relationship with heroes |

## Development Tools

- **Scalar API Reference**: Navigate to `/scalar` for interactive API documentation
- **Uvicorn**: ASGI server with auto-reload for development
- **Alembic**: Database migration management

## License

This project is for educational/assignment purposes.
