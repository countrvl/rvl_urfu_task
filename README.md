# Проект: TODO и ShortURL сервисы

## Описание
Проект состоит из двух микросервисов:

1. **TODO сервис**:
   - Позволяет управлять списком задач.
   - Реализованы CRUD-операции (создание, чтение, обновление, удаление задач).

2. **ShortURL сервис**:
   - Предоставляет возможность сокращать длинные URL.
   - Генерирует уникальные короткие ссылки и позволяет получить оригинальный URL по короткой ссылке.

---

## Запуск через Docker

### 1. TODO сервис

1. Скачайте образ:
   ```bash
   docker pull countrvl/todo-service:latest
   ```
2. Запустите контейнер:
   ```bash
   docker run -d -p 8000:80 countrvl/todo-service:latest
   ```
3. Тестирование:
   ```bash
   curl -X POST http://127.0.0.1:8000/items \
   -H "Content-Type: application/json" \
   -d '{"title": "Test Task", "description": "Testing TODO service", "completed": false}'
   ```

### 2. ShortURL сервис

1. Скачайте образ:
   ```bash
   docker pull countrvl/shorturl-service:latest
   ```
2. Запустите контейнер:
   ```bash
   docker run -d -p 8000:80 countrvl/shorturl-service:latest
   ```
3. Тестирование:
   ```bash
   curl -X POST http://127.0.0.1:8000/shorten \
   -H "Content-Type: application/json" \
   -d '{"url": "https://example.com"}'
   ```

---

## Тестирование с использованием скриптов

### TODO сервис
1. Запустите контейнер TODO сервиса:
   ```bash
   docker run -d -p 8000:80 countrvl/todo-service:latest
   ```
2. Выполните тестовый скрипт:
   ```bash
   bash ./todo/test_curl.sh
   ```

### ShortURL сервис
1. Запустите контейнер ShortURL сервиса:
   ```bash
   docker run -d -p 8000:80 countrvl/shorturl-service:latest
   ```
2. Выполните тестовый скрипт:
   ```bash
   bash ./short/test_curl_short.sh
   ```

---

## Эндпоинты 🫖 🙂

### TODO сервис
- **GET /items**: Получение списка всех задач.
- **POST /items**: Создание новой задачи.
  - Тело запроса:
    ```json
    {
      "title": "Название задачи",
      "description": "Описание задачи",
      "completed": false
    }
    ```
- **GET /items/{id}**: Получение задачи по ID.
- **PUT /items/{id}**: Обновление задачи по ID.
  - Тело запроса аналогично созданию задачи.
- **DELETE /items/{id}**: Удаление задачи по ID.

### ShortURL сервис
- **POST /shorten**: Создание короткого URL.
  - Тело запроса:
    ```json
    {
      "url": "https://example.com"
    }
    ```
- **GET /{short_id}**: Получение оригинального URL по короткому идентификатору.

---

## Структура проекта
```
project/
├── todo/
│   ├── DB/                    # База данных TODO сервиса
│   ├── main.py                # Основной файл TODO сервиса
│   ├── requirements.txt       # Зависимости TODO сервиса
│   ├── test_curl.sh           # Скрипт для тестирования TODO сервиса
│   ├── env.sample             # Пример переменных окружения TODO сервиса
│   └── Dockerfile             # Dockerfile для TODO сервиса
├── short/
│   ├── DB/                    # База данных ShortURL сервиса
│   ├── main.py                # Основной файл ShortURL сервиса
│   ├── requirements.txt       # Зависимости ShortURL сервиса
│   ├── test_curl_short.sh     # Скрипт для тестирования ShortURL сервиса
│   ├── env.sample             # Пример переменных окружения ShortURL сервиса
│   └── Dockerfile             # Dockerfile для ShortURL сервиса
├── README.md                   # Документация
└── .gitignore                  # Файл исключений для git
