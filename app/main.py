""" Main application file """

from fastapi.staticfiles import StaticFiles

from app.routes.home import app

app.mount("/app/static", app=StaticFiles(directory="app/static"), name="static")

# if __name__ == "__main__":
#     uvicorn.run("app/main:app", reload=True)
