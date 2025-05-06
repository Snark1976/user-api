FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-dev

COPY src /app/src
COPY migrations /app/migrations
COPY alembic.ini /app/alembic.ini

RUN poetry run litestar --app src.user_api.main:app database upgrade

CMD ["poetry", "run", "litestar", "--app", "src.user_api.main:app", "run", "--host", "0.0.0.0", "--port", "8000"]
