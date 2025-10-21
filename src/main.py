
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

from src.api.chat import router as chat_router

app = FastAPI()

# Mount API router under /api
app.include_router(chat_router, prefix="/api")

# Static files and templates
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
async def read_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})