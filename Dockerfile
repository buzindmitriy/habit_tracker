# Базовый образ
FROM python:3.11-slim

# Установка рабочей директории
WORKDIR /app

# Установка Poetry через официальный скрипт
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

# Проверка установки Poetry
RUN poetry --version

# Копирование файлов Poetry
COPY pyproject.toml poetry.lock ./

# Установка зависимостей
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

# Копирование остальных файлов проекта
COPY . .

# Открытие порта
EXPOSE 8000

# Команда по умолчанию (можно переопределить в docker-compose.yaml)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]