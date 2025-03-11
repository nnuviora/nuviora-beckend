# Використовуємо базовий образ
FROM python:3.10-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файл з залежностями
COPY requirements.txt /app/

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код в контейнер
COPY . /app/

# Відкриваємо порт для роботи додатка
EXPOSE 8080

# Команда для запуску додатка
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

