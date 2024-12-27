
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from tortoise.models import Model
from tortoise import Tortoise, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from dotenv import load_dotenv
import os

os.makedirs("DB", exist_ok=True)

load_dotenv()  
DB_URL = os.getenv("TODO_DB_URL", "sqlite://./DB/todo.db")

async def lifespan(app: FastAPI):
    await Tortoise.init(db_url=DB_URL, modules={"models": ["main"]})
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

app_todo = FastAPI(lifespan=lifespan)

class TodoItem(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    completed = fields.BooleanField(default=False)

# Pydantic models
TodoItem_Pydantic = pydantic_model_creator(TodoItem, name="TodoItem")
TodoItemIn_Pydantic = pydantic_model_creator(TodoItem, name="TodoItemIn", exclude_readonly=True)

@app_todo.post("/items", response_model=TodoItem_Pydantic)
async def create_todo_item(item: TodoItemIn_Pydantic):
    todo = await TodoItem.create(**item.dict())
    return await TodoItem_Pydantic.from_tortoise_orm(todo)

@app_todo.get("/items", response_model=List[TodoItem_Pydantic])
async def get_todo_items():
    return await TodoItem_Pydantic.from_queryset(TodoItem.all())

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

@app_todo.delete("/items/{item_id}", response_model=dict)
async def delete_todo_item(item_id: int):
    todo = await TodoItem.get_or_none(id=item_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Item not found")
    await todo.delete()
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_todo, host="0.0.0.0", port=8000)
