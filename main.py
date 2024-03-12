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

@app.post("/", response_class=RedirectResponse)
async def create_opinion(request: Request, text: str = Form(...), category: str = Form(...), user: str = Form(...)):
    opinion = Opinion(text=text, category=category, user=user)
    opinions.insert(0, opinion)
    return RedirectResponse(url="/opinions", status_code=303)


@app.get("/opinions", response_class=HTMLResponse)
async def show_opinions(request: Request, page: int = 1):
    items_per_page = 10
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    total_opinions = len(opinions)
    total_pages = (total_opinions - 1) // items_per_page + 1

    paginated_opinions = opinions[start_index:end_index]

    return templates.TemplateResponse("opinions.html", {"request": request, "opinions": paginated_opinions, "page": page, "total_pages": total_pages})

@app.get("/user/{username}", response_class=HTMLResponse)
async def show_user_opinions(request: Request, username: str):
    user_opinions = [opinion for opinion in opinions if opinion.user == username]
    return templates.TemplateResponse("user_opinions.html", {"request": request, "username": username, "user_opinions": user_opinions})
