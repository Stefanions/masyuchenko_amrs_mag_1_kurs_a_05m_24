# Базовый образ для сборки Python-приложения
FROM python:3.9.13 as base

# Установка зависимостей
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Этап тестирования
FROM base AS test
COPY . .
CMD pytest app/tests/

# Этап production
FROM base AS production
COPY . .
CMD ["python", "app/main.py"]