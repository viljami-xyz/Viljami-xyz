""" Main application file """

from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db.handler import (
    create_db_and_tables,
    get_repositories,
    requires_update,
    set_updated,
    update_table,
)
from app.db.models import ApiName, Repositories
from app.services.github import get_repository_data
from app.services.goodreads import GoodReadsBooks

templates = Jinja2Templates(directory="app/templates")

books_loader = GoodReadsBooks()

app = FastAPI()

app.mount("/app/static", app=StaticFiles(directory="app/static"), name="static")


@app.get("/")
def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/projects")
async def get_projects(request: Request, lang: str = None):
    """print projects"""
    req_projects = await get_repositories()
    req_projects = [project.__dict__ for project in req_projects]
    if lang and lang != "all":
        req_projects = [
            project for project in req_projects if lang in project["languages"].keys()
        ]
    return templates.TemplateResponse(
        "projects/projectCardList.html", {"request": request, "projects": req_projects}
    )


@app.get("/projects/pre-load")
async def projects_preload():
    """preload projects"""
    if await requires_update(ApiName.REPOSITORIES):
        repos = get_repository_data()
        await update_table(repos, Repositories)
        await set_updated(ApiName.REPOSITORIES)
    return None


@app.get("/projects/first-load")
async def projects_firstload(request: Request, lang: str = None):
    """print projects"""
    req_projects = await get_repositories()
    req_projects = [project.__dict__ for project in req_projects]
    if lang and lang != "all":
        req_projects = [
            project for project in req_projects if lang in project["languages"].keys()
        ]

    return templates.TemplateResponse(
        "projects/projectCardList.html", {"request": request, "projects": req_projects}
    )


@app.get("/books")
async def get_books(request: Request):
    """print projects"""
    books = await books_loader.fetch_books()
    return templates.TemplateResponse(
        "books/booksList.html", {"request": request, "books": books}
    )


@app.post("/books/show")
async def show_book(
    request: Request, book_title: str = Form(...), book_author: str = Form(...)
):
    """print projects"""

    return templates.TemplateResponse(
        "books/show.html",
        {"request": request, "title": book_title, "author": book_author},
    )


@app.on_event("startup")
async def startup_event():
    """Create database and tables"""
    await create_db_and_tables()
