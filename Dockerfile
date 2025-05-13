# Базовый образ
FROM python:3.11-slim

# Установка рабочей директории
WORKDIR /app

# Установка Poetry и зависимостей
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org  | python3 -
ENV PATH="${PATH}:/root/.local/bin"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

# Копирование остальных файлов
COPY . .

# Сборка статики и миграции
RUN python manage.py collectstatic --noinput && \
    python manage.py makemigrations && \
    python manage.py migrate

# Открытие порта
EXPOSE 8000

# Команда для запуска приложения через Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]