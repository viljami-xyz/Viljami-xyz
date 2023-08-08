""" Main application file """

from celery import Celery
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db.handler import (
    async_get_books,
    async_get_repositories,
    create_db_and_tables,
    set_updated,
    update_table,
)
from app.db.models import ApiName, Books, Repositories
from app.services.github import get_repository_data
from app.services.goodreads import fetch_books, nested_books
from app.services.models import repo_from_orm

templates = Jinja2Templates(directory="app/templates")


app = FastAPI()


celery = Celery("tasks")
celery.config_from_object("celeryconfig")

app.mount("/app/static", app=StaticFiles(directory="app/static"), name="static")


@app.get("/")
def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/projects")
async def get_projects(request: Request, lang: str = None):
    """print projects"""
    req_projects = await async_get_repositories()
    req_projects = [repo_from_orm(project) for project in req_projects]
    if lang and lang != "all":
        req_projects = [
            project for project in req_projects if lang in project.languages.keys()
        ]
    return templates.TemplateResponse(
        "projects/projectCardList.html", {"request": request, "projects": req_projects}
    )


@app.get("/projects/pre-load")
def projects_preload():
    """preload projects"""
    # if requires_update(ApiName.REPOSITORIES):
    #     repos = get_repository_data()
    #     update_table(repos, Repositories)
    #     set_updated(ApiName.REPOSITORIES)
    return None


@app.get("/projects/first-load")
async def projects_firstload(request: Request, lang: str = None):
    """print projects"""
    req_projects = await async_get_repositories()
    req_projects = [repo_from_orm(project) for project in req_projects]
    if lang and lang != "all":
        req_projects = [
            project for project in req_projects if lang in project.languages.keys()
        ]

    return templates.TemplateResponse(
        "projects/projectCardList.html", {"request": request, "projects": req_projects}
    )


@app.get("/books")
async def get_books(request: Request):
    """print projects"""
    books = await async_get_books()
    books = nested_books(books)
    return templates.TemplateResponse(
        "books/booksList.html", {"request": request, "books": books}
    )


@app.post("/books/show")
def show_book(
    request: Request, book_title: str = Form(...), book_author: str = Form(...)
):
    """print projects"""

    return templates.TemplateResponse(
        "books/show.html",
        {"request": request, "title": book_title, "author": book_author},
    )


@celery.task(name="scheduled_update")
def update_database_task():
    """Update database"""
    update_table(get_repository_data(), Repositories)
    update_table(fetch_books(), Books)
    set_updated(ApiName.REPOSITORIES)
    set_updated(ApiName.BOOKS)


@app.post("/update-db")
def trigger_update():
    """Update database"""
    update_database_task.delay()


@app.on_event("startup")
def startup_event():
    """Create database and tables"""
    create_db_and_tables()
