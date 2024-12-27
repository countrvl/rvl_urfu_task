from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from tortoise.models import Model
from tortoise import Tortoise, fields
from dotenv import load_dotenv
import os

app_todo = FastAPI()

load_dotenv()  # Load environment variables
DB_URL = os.getenv("TODO_DB_URL")

class TodoItem(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    completed = fields.BooleanField(default=False)

@app_todo.on_event("startup")
async def init_db():
    await Tortoise.init(
        db_url=DB_URL, modules={"models": ["__main__"]}
    )
    await Tortoise.generate_schemas()

@app_todo.post("/items")
async def create_todo_item(item: BaseModel):
    todo = await TodoItem.create(**item.dict())
    return {"message": "Task created successfully", "id": todo.id}

@app_todo.get("/items", response_model=List[BaseModel])
async def get_todo_items():
    todos = await TodoItem.all()
    return todos

@app_todo.get("/items/{item_id}")
async def get_todo_item(item_id: int):
    todo = await TodoItem.get_or_none(id=item_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Item not found")
    return todo

@app_todo.put("/items/{item_id}")
async def update_todo_item(item_id: int, item: BaseModel):
    todo = await TodoItem.get_or_none(id=item_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Item not found")
    await todo.update_from_dict(item.dict()).save()
    return {"message": "Task updated successfully"}

@app_todo.delete("/items/{item_id}")
async def delete_todo_item(item_id: int):
    todo = await TodoItem.get_or_none(id=item_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Item not found")
    await todo.delete()
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_todo, host="0.0.0.0", port=8000)

