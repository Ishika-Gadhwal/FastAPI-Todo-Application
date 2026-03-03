

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Path, Query, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from passlib.context import CryptContext

from starlette import status

from models import Users

from database import sessionLocal
from sqlalchemy.orm import Session

# For authenticating User
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# For creating the json web token and return it to the client
from jose import JWTError, jwt

# Making templates for full stack application
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from config import SECRET_KEY

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

# Making Json web Token
# SECRET_KEY = SECRET_KEY
ALGORITHM = "HS256"
# Now these both will provide the signature for JWT token so that JWT is secured and authorized

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
#Decode a Jwt toke so that we an use it to authenticate a user by verifying it's JWT token
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class UsersRequestModel(BaseModel):
    email : str
    username: str
    first_name : str
    last_name : str
    password : str
    role: str
    phone_number : str = Field(max_length=10,min_length=10)
    
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

# Using templates for full stack application
templates = Jinja2Templates(directory="templates")

### PAGES ###

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


### Endpoints ###

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user
        

def create_JWT_token(username: str, user_id: int, role: str ,expires_delta: timedelta):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode['exp'] = expires
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role : str = payload.get("role")
        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user.")
        return {'username': username, 'id':user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user.")


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, user_request: UsersRequestModel):
    new_user = Users(
        email = user_request.email,
        username = user_request.username,
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        role = user_request.role,
        hashed_password = bcrypt_context.hash(user_request.password),
        is_active = True,
        phone_number = user_request.phone_number
    )
    
    db.add(new_user)
    db.commit()
    
    
@router.post("/token")
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user.")
    
    token = create_JWT_token(user.username, user.id, user.role,timedelta(minutes=11))
    # This token will be expires after 11 minutes
    return {"access_token": token, "token_type": "bearer"}
    