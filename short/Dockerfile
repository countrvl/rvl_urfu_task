# Используем официальный Python-образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Устанавливаем переменную окружения для базы данных
ENV SHORT_DB_URL=sqlite://./DB/shorturl.db

# Указываем порт, который будет использовать приложение
EXPOSE 80

# Убедимся, что папка для базы данных существует
RUN mkdir -p /app/DB

# Команда запуска приложения
CMD ["uvicorn", "main:app_short", "--host", "0.0.0.0", "--port", "80"]
