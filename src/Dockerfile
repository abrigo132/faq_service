FROM python:3.11-slim

WORKDIR /src
# Установка Poetry
RUN pip install poetry

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock* ./

# Установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Копирование исходного кода
COPY . .

# Команда запуска
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]