klcreke# Описание проектов TODO и ShortURL

## Описание

### TODO
TODO-сервис предоставляет базовый функционал для управления задачами:
- Создание задач.
- Изменение задач.
- Удаление задач.
- Получение списка задач или отдельной задачи по идентификатору.

### ShortURL
ShortURL-сервис предоставляет возможность сокращать длинные URL-адреса и получать их по коротким ссылкам:
- Генерация уникального короткого идентификатора для URL.
- Перенаправление по короткой ссылке на исходный URL.

---

## Запуск через Docker

### Требования
- Установленный Docker.

### Запуск контейнеров

1. Запустите TODO-сервис:
   ```bash
   docker run -d -p 8000:80 -v todo_data:/app/DB countrvl/todo-service:latest
   ```

2. Запустите ShortURL-сервис:
   ```bash
   docker run -d -p 8001:80 -v shorturl_data:/app/DB countrvl/shorturl-service:latest
   ```

---

## Эндпоинты, а по олдскулу ручки :)

### TODO-сервис
- **GET /items** - Получить все задачи.
- **POST /items** - Создать новую задачу.
  Пример тела запроса:
  ```json
  {
    "title": "Купить продукты",
    "description": "Молоко, яйца, хлеб",
    "completed": false
  }
  ```
- **GET /items/{id}** - Получить задачу по идентификатору.
- **PUT /items/{id}** - Обновить задачу.
  Пример тела запроса:
  ```json
  {
    "title": "Обновлённая задача",
    "description": "Обновлённое описание",
    "completed": true
  }
  ```
- **DELETE /items/{id}** - Удалить задачу по идентификатору.

### ShortURL-сервис
- **POST /shorten** - Создать короткий URL.
  Пример тела запроса:
  ```json
  {
    "url": "https://example.com"
  }
  ```
  Пример ответа:
  ```json
  {
    "id": 1,
    "short_id": "abc123",
    "original_url": "https://example.com"
  }
  ```
- **GET /{short_id}** - Перенаправление на оригинальный URL.

---

## Примеры запросов

### TODO-сервис
- Создание задачи:
  ```bash
  curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"title": "Купить продукты", "description": "Молоко, яйца", "completed": false}'
  ```

- Получение всех задач:
  ```bash
  curl -X GET http://localhost:8000/items
  ```

### ShortURL-сервис
- Создание короткого URL:
  ```bash
  curl -X POST http://localhost:8001/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
  ```

- Получение оригинального URL:
  ```bash
  curl -X GET http://localhost:8001/abc123
  ```

---

## Тестовые скрипты

### TODO-сервис
После запуска контейнера с TODO-сервисом вы можете выполнить тестирование с помощью скрипта:
```bash
./test_todo.sh
```
Тест проверяет создание, получение, обновление и удаление задач.

### ShortURL-сервис
После запуска контейнера с ShortURL-сервисом вы можете выполнить тестирование с помощью скрипта:
```bash
./test_curl_short.sh
```
Тест проверяет создание коротких ссылок и их корректное перенаправление.
