import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from backend import models, database, endpoints
from dotenv import load_dotenv

load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Define the base directory (project root)
BASE_DIR = Path(__file__).resolve().parent.parent

# Configure templates and static directories using absolute paths
templates = Jinja2Templates(directory=str(BASE_DIR / "frontend" / "templates"))
static_dir = str(BASE_DIR / "frontend" / "static")

# Mount the static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include API endpoints (no additional prefix here)
app.include_router(endpoints.router)

# Main page
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Configuration test page to verify endpoints and static file serving
@app.get("/config-test")
def config_test(request: Request):
    return templates.TemplateResponse("config_test.html", {"request": request})
