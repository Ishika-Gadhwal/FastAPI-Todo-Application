from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from models import Todos, Users
from database import sessionLocal
from sqlalchemy.orm import Session

from starlette import status

from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != 'admin':
        raise HTTPException(status_code=401,detail="Authentication Failed")
    return db.query(Todos).all()


@router.delete("/delete_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get("user_role") != 'admin':
        raise HTTPException(status_code=401,detail="Authentication Failed")
    
    todo_record = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_record is None:
        raise HTTPException(status_code=404, detail=f"No Todo with Todo id : {todo_id} is found ")
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
        
# get_user: this endpoint should return all information about the user that is currently logged in.
@router.get("/get_user",status_code=status.HTTP_200_OK)
async def get_all_user(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != 'admin':
        raise HTTPException(status_code=401,detail="Authentication Failed")
    return db.query(Users).all()