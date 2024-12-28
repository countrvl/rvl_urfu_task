from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tortoise.models import Model
from tortoise import Tortoise, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from dotenv import load_dotenv
import os
import random
import string

# Ensure the DB folder exists
os.makedirs("DB", exist_ok=True)

# Load environment variables
load_dotenv()
DB_URL = os.getenv("SHORT_DB_URL", "sqlite://./DB/shorturl.db")

# Initialize FastAPI
app_short = FastAPI()

# Tortoise ORM lifespan
async def lifespan(app: FastAPI):
    try:
        print(f"Initializing database with URL: {DB_URL}")
        await Tortoise.init(db_url=DB_URL, modules={"models": ["__main__"]})
        await Tortoise.generate_schemas()
        print("Database initialized successfully.")
        yield
    finally:
        await Tortoise.close_connections()

app_short = FastAPI(lifespan=lifespan)

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
class URLRequest(BaseModel):
    url: str

@app_short.get("/teapot", status_code=418) # :)
async def teapot():
    return {"detail": "I'm a teapot"}

@app_short.post("/shorten", response_model=ShortURL_Pydantic)
async def shorten_url(request: URLRequest):
    try:
        short_id = generate_short_id()
        print(f"Generated short_id: {short_id} for URL: {request.url}")
        short_url = await ShortURL.create(short_id=short_id, original_url=request.url)
        print(f"Shortened URL created: {short_url.short_id} -> {short_url.original_url}")
        return await ShortURL_Pydantic.from_tortoise_orm(short_url)
    except Exception as e:
        print(f"Error during URL shortening: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# API to redirect to the original URL
@app_short.get("/{short_id}")
async def redirect_to_url(short_id: str):
    short_url = await ShortURL.get_or_none(short_id=short_id)
    if not short_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    print(f"Redirecting short_id: {short_id} to URL: {short_url.original_url}")
    return {"original_url": short_url.original_url}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_short, host="0.0.0.0", port=8000)
