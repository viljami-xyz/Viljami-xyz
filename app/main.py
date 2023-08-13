""" Main application file """

from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db.handler import (
    async_get_books,
    async_get_education,
    async_get_jobs,
    async_get_repositories,
    create_db_and_tables,
)
from app.services.goodreads import nested_books
from app.services.linkedin import modeled_education, modeled_jobs
from app.services.models import repo_from_orm

templates = Jinja2Templates(directory="app/templates")


app = FastAPI()


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
        "projects/projectCardList.html.j2",
        {"request": request, "projects": req_projects},
    )


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
        "projects/projectCardList.html.j2",
        {"request": request, "projects": req_projects},
    )


@app.get("/books")
async def get_books(request: Request):
    """print projects"""
    books = await async_get_books()
    books = nested_books(books)
    return templates.TemplateResponse(
        "books/booksList.html.j2", {"request": request, "books": books}
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


@app.get("/jobs")
async def get_jobs(request: Request):
    """print jobs"""
    jobs = await async_get_jobs()
    jobs = modeled_jobs(jobs)

    return templates.TemplateResponse(
        "jobs/jobCardList.html.j2", {"request": request, "jobs": jobs}
    )


@app.get("/education")
async def get_education(request: Request):
    """print jobs"""
    education = await async_get_education()
    education = modeled_education(education)
    return templates.TemplateResponse(
        "education/educationCardList.html.j2",
        {"request": request, "education": education},
    )


@app.on_event("startup")
def startup_event():
    """Create database and tables"""
    create_db_and_tables()
