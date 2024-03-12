from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Opinion(BaseModel):
    text: str
    category: str
    user: str

opinions = []

@app.get("/", response_class=HTMLResponse)
async def read_opinions(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
