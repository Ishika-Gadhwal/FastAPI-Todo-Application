

from fastapi import FastAPI, Request, status
import models
from database import engine

from routers import auth, todos, admin

from fastapi.staticfiles import StaticFiles

from fastapi.responses import RedirectResponse


app = FastAPI()

# This will only run when todos.db is not created in the folder
models.Base.metadata.create_all(bind=engine)


# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# # Making templates for full stack application
# templates = Jinja2Templates(directory="templates")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code = status.HTTP_302_FOUND)
    

# Only router in main file and all the routes and endpoints will be shifted to routers folder and their files
# Now , include the router for authentication and authorization
app.include_router(auth.router)
app.include_router(todos.router) 
app.include_router(admin.router)
