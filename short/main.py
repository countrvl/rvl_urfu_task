from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from tortoise.models import Model
from tortoise import Tortoise, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from dotenv import load_dotenv
import os
import random
import string

# Load environment variables
load_dotenv()
DB_URL = os.getenv("SHORT_DB_URL", "sqlite://./DB/shorturl.db")

# Initialize FastAPI
app = FastAPI()

# Tortoise ORM lifespan
async def lifespan(app: FastAPI):
    await Tortoise.init(db_url=DB_URL, modules={"models": ["main"]})
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

app = FastAPI(lifespan=lifespan)

# Database model
class ShortURL(Model):
    id = fields.IntField(pk=True)
    short_id = fields.CharField(max_length=8, unique=True)
    original_url = fields.TextField()

# Pydantic models
ShortURL_Pydantic = pydantic_model_creator(ShortURL, name="ShortURL")
ShortURLIn_Pydantic = pydantic_model_creator(ShortURL, name="ShortURLIn", exclude_readonly=True)

# Helper to generate short IDs
def generate_short_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# API to shorten URLs
@app.post("/shorten", response_model=ShortURL_Pydantic)
async def shorten_url(url: str):
    short_id = generate_short_id()
    short_url = await ShortURL.create(short_id=short_id, original_url=url)
    return await ShortURL_Pydantic.from_tortoise_orm(short_url)

# API to redirect to the original URL
@app.get("/{short_id}")
async def redirect_to_url(short_id: str):
    short_url = await ShortURL.get_or_none(short_id=short_id)
    if not short_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return {"original_url": short_url.original_url}
