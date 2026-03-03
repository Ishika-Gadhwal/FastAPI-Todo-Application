



from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from pydantic import BaseModel, Field
from models import Todos, Users
from database import sessionLocal
from sqlalchemy.orm import Session

from starlette import status

from .auth import get_current_user

from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# Making templates for full stack application
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

def get_db():   
    db = sessionLocal() # taking local todos database in db -> connect to database
    try:
        yield db # return todos database
    finally:
        db.close() # close todos database and return all the information
        

db_dependency = Annotated[Session, Depends(get_db)]  # Depends is the dependency injection i.e; work that we want to do first behind the scene
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequestModel(BaseModel):
    title: str = Field(min_length=3, max_length=33)
    description: str = Field(min_length=5, max_length=55)
    priority: int = Field(gt=0, le=5)
    complete: bool = Field(default=False)
    
class ChangePasswordRequest(BaseModel):
    new_password: str = Field(min_length=6)
    
    
# For making Full stack Application
def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response
    
### PAGES ###
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        
        if user is None:
            return redirect_to_login()
        
        todos = db.query(Todos).filter(Todos.owner == user.get("id")).all()
        
        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})
    except:
        return redirect_to_login()
    
    
@router.get("/add-todo-page")
async def render_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        
        if user is None:
            return redirect_to_login()
        
        return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})
    
    except:
        return redirect_to_login()
    

@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        
        if user is None:
            return redirect_to_login()
        
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        
        return templates.TemplateResponse("edit-todo.html", {"request":request, "todo": todo, "user":user})
    
    except:
        return redirect_to_login()

### Endpoints ###        
@router.get("/", status_code=status.HTTP_200_OK) # Endpoint to get all the data from database
async def read_all(user: user_dependency, db: db_dependency):
    # db_dependency Means read_all() function depends on get_db() which is responsible fr opening and closing the database
    
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    
    return db.query(Todos).filter(Todos.owner == user.get('id')).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_one_todo(user: user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    
    todo_record = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner == user.get('id')).first()
    if todo_record:
        return todo_record
    raise HTTPException(status_code=404, detail=f"No Todo with Todo id : {todo_id} is found ")


@router.post("/create_todo",status_code=status.HTTP_201_CREATED)
async def create_new_todo(user: user_dependency,db: db_dependency, todo_request: TodoRequestModel):
    
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    
    new_todo = Todos(**todo_request.model_dump(), owner=user.get('id'))
    
    db.add(new_todo)
    db.commit()
    
    
@router.put("/update_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todos(user: user_dependency, db: db_dependency ,todo_request: TodoRequestModel, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    
    new_todo = Todos(**todo_request.model_dump())
    
    todo_record = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner == user.get("id")).first()

    if todo_record is None:
        raise HTTPException(status_code=404, detail=f"No Todo with Todo id : {todo_id} is found ")
    
    todo_record.title = new_todo.title
    todo_record.description = new_todo.description
    todo_record.priority = new_todo.priority
    todo_record.complete = new_todo.complete
    
    db.add(todo_record)
    db.commit()
    
    
@router.delete("/delete_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todos(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    
    todo_record = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner==user.get("id")).first()
    if todo_record is None:
        raise HTTPException(status_code=404, detail=f"No Todo with Todo id : {todo_id} is found ")
    
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner==user.get("id")).delete()
    db.commit()
    
    
# change_password: this endpoint should allow a user to change their current password.
@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_my_password(user: user_dependency, db: db_dependency, password_data: ChangePasswordRequest):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    
    user_info = db.query(Users).filter(Users.id == user.get("id")).first()
    
    if user_info is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_info.hashed_password = bcrypt_context.hash(password_data.new_password)
    db.add(user_info)
    db.commit()
    
    
# Create a new @put request in our users.py file that allows a user to update their phone_number
@router.put("/change_phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_my_phone_number(user: user_dependency, db: db_dependency, phone_number_data: str = Query(max_length=10,min_length=10)):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    
    user_info = db.query(Users).filter(Users.id == user.get("id")).first()
    
    if user_info is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_info.phone_number = phone_number_data
    db.add(user_info)
    db.commit()