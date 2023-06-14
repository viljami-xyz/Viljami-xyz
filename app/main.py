""" Main application file """

from fastapi.staticfiles import StaticFiles

from app.routes.home import app
from app.routes.projects import router as projects_router

app.mount("/app/static", app=StaticFiles(directory="app/static"), name="static")

app.include_router(projects_router)

# if __name__ == "__main__":
#     uvicorn.run("app/main:app", reload=True)
