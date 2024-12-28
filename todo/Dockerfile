FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Указываем порт
EXPOSE 80

# Запускаем приложение
CMD ["uvicorn", "main:app_todo", "--host", "0.0.0.0", "--port", "80"]
