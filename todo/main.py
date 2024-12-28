from fastapi import FastAPI, HTTPException
from tortoise.models import Model
from tortoise import Tortoise, fields
from tortoise.contrib.pydantic import pydantic_model_creator
import os

# Убедимся, что папка DB существует
os.makedirs("DB", exist_ok=True)

# Конфигурация базы данных
TODO_DB_URL = "sqlite://./DB/todo.db"

# Инициализация FastAPI
app_todo = FastAPI()

# ORM lifespan
async def lifespan(app: FastAPI):
    try:
        print(f"Initializing database with URL: {TODO_DB_URL}")
        await Tortoise.init(db_url=TODO_DB_URL, modules={"models": ["__main__"]})
        await Tortoise.generate_schemas()
        print(f"Connected to database: {TODO_DB_URL}")
        yield
    except Exception as e:
        print(f"Error during lifespan startup: {e}")
        raise
    finally:
        await Tortoise.close_connections()

app_todo = FastAPI(lifespan=lifespan)

# Модель базы данных
class TodoItem(Model):
    id = fields.IntField(pk=True)
    title = fields.TextField()
    description = fields.TextField(null=True)
    completed = fields.BooleanField(default=False)

# Pydantic модели
TodoItem_Pydantic = pydantic_model_creator(TodoItem, name="TodoItem")
TodoItemIn_Pydantic = pydantic_model_creator(TodoItem, name="TodoItemIn", exclude_readonly=True)

# Эндпоинты
@app_todo.get("/teapot", status_code=418) # :)
async def teapot():
    return {"detail": "I'm a teapot"}

@app_todo.get("/items")
async def get_todo_items():
    return await TodoItem_Pydantic.from_queryset(TodoItem.all())

@app_todo.post("/items", response_model=TodoItem_Pydantic)
async def create_todo_item(item: TodoItemIn_Pydantic):
    todo = await TodoItem.create(**item.dict())
    return await TodoItem_Pydantic.from_tortoise_orm(todo)

@app_todo.get("/items/{item_id}", response_model=TodoItem_Pydantic)
async def get_todo_item(item_id: int):
    todo = await TodoItem.get_or_none(id=item_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Item not found")
    return await TodoItem_Pydantic.from_tortoise_orm(todo)

@app_todo.put("/items/{item_id}", response_model=TodoItem_Pydantic)
async def update_todo_item(item_id: int, item: TodoItemIn_Pydantic):
    todo = await TodoItem.get_or_none(id=item_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Item not found")
    await todo.update_from_dict(item.dict()).save()
    return await TodoItem_Pydantic.from_tortoise_orm(todo)

@app_todo.delete("/items/{item_id}")
async def delete_todo_item(item_id: int):
    todo = await TodoItem.get_or_none(id=item_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Item not found")
    await todo.delete()
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_todo, host="0.0.0.0", port=8000)
