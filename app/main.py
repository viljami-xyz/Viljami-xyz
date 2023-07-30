""" Main application file """

from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.github import GithubRepos
from app.services.goodreads import GoodReadsBooks

templates = Jinja2Templates(directory="app/templates")

repo_loader = GithubRepos()
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
    req_projects = repo_loader.repository_data
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
    _ = repo_loader.repository_data
    return None


@app.get("/projects/first-load")
async def projects_firstload(request: Request, lang: str = None):
    """print projects"""
    req_projects = repo_loader.load_repositories
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
