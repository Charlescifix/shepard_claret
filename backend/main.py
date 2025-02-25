from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import pathlib

app = FastAPI()

# Calculate absolute paths relative to this file's parent directory
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
templates_dir = BASE_DIR / "frontend" / "templates"
static_dir = BASE_DIR / "frontend" / "static"

# Mount static files
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(templates_dir))

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
