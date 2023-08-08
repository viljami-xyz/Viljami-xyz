""" Main application file """

from celery import Celery
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db.handler import (
    async_get_books,
    async_get_education,
    async_get_jobs,
    async_get_repositories,
    create_db_and_tables,
    set_updated,
    update_table,
)
from app.db.models import ApiName, Books, Education, Jobs, Repositories
from app.services.github import get_repository_data
from app.services.goodreads import fetch_books, nested_books
from app.services.linkedin import modeled_education, modeled_jobs, user_profile
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


@app.get("/jobs")
async def get_jobs(request: Request):
    """print jobs"""
    jobs = await async_get_jobs()
    jobs = modeled_jobs(jobs)

    return templates.TemplateResponse(
        "jobs/jobCardList.html", {"request": request, "jobs": jobs}
    )


@app.get("/education")
async def get_education(request: Request):
    """print jobs"""
    education = await async_get_education()
    education = modeled_education(education)
    return templates.TemplateResponse(
        "education/educationCardList.html", {"request": request, "education": education}
    )


@celery.task(name="scheduled_update")
def update_database_task():
    """Update database"""

    # Update tables
    update_table(get_repository_data(), Repositories)
    update_table(fetch_books(), Books)
    linkedin_profile = user_profile()
    update_table(linkedin_profile["jobs"], Jobs)
    update_table(linkedin_profile["education"], Education)
    # Mark all tables as updated
    set_updated(ApiName.REPOSITORIES)
    set_updated(ApiName.BOOKS)
    set_updated(ApiName.JOBS)
    set_updated(ApiName.EDUCATION)


@app.post("/update-db")
def trigger_update():
    """Update database"""
    update_database_task.delay()


@app.on_event("startup")
def startup_event():
    """Create database and tables"""
    create_db_and_tables()
