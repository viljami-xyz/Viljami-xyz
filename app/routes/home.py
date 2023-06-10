from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})
