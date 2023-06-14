""" This file contains the routes for the projects page. """

import json
import pathlib

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

projects = json.loads(
    pathlib.Path("app/static/projects.json").read_text(encoding="utf-8")
)
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
async def get_projects(request: Request, stack: str = None):
    """print projects"""
    req_projects = projects
    if stack and stack != "all":
        req_projects = [
            project for project in req_projects if project["stack"] == stack
        ]
    return templates.TemplateResponse(
        "projects/projectCardList.html", {"request": request, "projects": req_projects}
    )
