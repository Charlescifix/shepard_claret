from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from backend import models, database, endpoints
from dotenv import load_dotenv
import os

load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Include API endpoints
app.include_router(endpoints.router)

# Setup templates and static files
templates = Jinja2Templates(directory="frontend/templates")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
