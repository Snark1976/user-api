# User API Project

## Overview
This project is a REST API built with LiteStar (version 2.x) and Python 3.12, implementing CRUD operations for a `user` table. The API includes Swagger documentation, unit tests with Pytest, and supports Docker for deployment with PostgreSQL. The project uses Poetry (1.8.3) as the dependency manager, Alembic for database migrations, and follows a modular structure with the `src/user_api` package.

### Features
- CRUD operations for `user` table (id, name, surname, password, created_at, updated_at).
- Swagger UI for API documentation.
- Unit tests with Pytest.
- Support for console and Docker-based execution.
- Database migrations with Alembic (supports PostgreSQL).

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Snark1976/user-api.git
   cd user-api
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```
   If you modify dependencies in `pyproject.toml`, run the following to update the lock file:
   ```bash
   poetry lock
   poetry install
   ```
3. Copy the example environment file and rename it:
   ```bash
   copy .env.example .env
   ```
   Edit `DATABASE_URL` in `.env` to match your PostgreSQL setup. Example:
   ```bash
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/user_db
   ```
4. Apply database migrations:
   ```bash
   litestar --app src.user_api.main:app database upgrade
   ```

## Running the Application

### Via Console
Run the application:
```bash
litestar --app src.user_api.main:app run --host 0.0.0.0 --port 8000
```

### Via Docker
Build and run the container:
```bash
docker-compose up --build
```

Access the API at `http://localhost:8000` and Swagger at `http://localhost:8000/schema`.

## Running Tests
Execute tests with:
```bash
poetry run pytest
```

## Database Migrations
- To create a new migration after changing models:
  ```bash
  litestar --app src.user_api.main:app database revision --autogenerate -m "Description of changes"
  ```
- To apply migrations:
  ```bash
  litestar --app src.user_api.main:app database upgrade
  ```
- If using Docker, apply migrations inside the container:
  ```bash
  docker-compose exec app litestar --app src.user_api.main:app database upgrade
  ```

## Notes
- The `.env` file must exist and contain a valid `DATABASE_URL`.
