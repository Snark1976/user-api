FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --without dev

CMD ["poetry", "run", "litestar", "--app", "src.user_api.main:app", "run", "--host", "0.0.0.0", "--port", "8000"]
