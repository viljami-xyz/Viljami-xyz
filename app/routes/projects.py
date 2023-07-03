""" This file contains the routes for the projects page. """

import json
import pathlib

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.github import GithubRepos

repo_loader = GithubRepos()
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
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


@router.get("/pre-load")
async def projects_preload():
    """preload projects"""
    repo_loader.repository_data
    return None


@router.get("/first-load")
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
