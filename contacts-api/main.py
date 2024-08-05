from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from pydantic import BaseModel
from routers import contacts
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError

from enum import Enum

from typing_extensions import Annotated

TOKEN_EXPIRATION_MINUTES = 1
SECRET_KEY = '9e599617f42ea3f7fbb58f4566d31b72c1970323a68d65cd8fa3258483ecfdb3'
ALGORITH = 'HS256'

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

app = FastAPI()

app.include_router(contacts.router)

class User(BaseModel):
    username: str
    phone: str
    email: str
    age: int
    disabled: bool


class UserInDB(User):
    hashed_password: str

# predefined values
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# fake users db

fake_users_db = {
    "jhondoe": {
        "username": "jhondoe",
        "phone": "77074485",
        "email": "jhondoe@gmail.com",
        "age": 19,
        "disabled": False,
        "hashed_password": "$2a$12$6hm7P/fHg8Wjg72uewCHau9trXznBf/bc9nsxv5e8m/2GFqdVktGW"
    },
    "alice": {
        "username": "alice",
        "phone": "77074159",
        "email": "alice@gmail.com",
        "age": 15,
        "disabled": True,
        "hashed_password": "$2a$12$6hm7P/fHg8Wjg72uewCHau9trXznBf/bc9nsxv5e8m/2GFqdVktGW"
    }
}

def fake_hash_password(password):
    return "fakehashed" + password

def get_user(db, username):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_excepion =  HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials.',
            headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITH])
        username = payload.get("username")
        if username is None:
            raise credentials_excepion

    except InvalidTokenError:
        print('exception found')
        raise credentials_excepion
    
    user = get_user(fake_users_db, username)
    
    if user is None:
        raise credentials_excepion
    
    return user
    

def get_current_active_user(user: User = Depends(get_current_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Inactive user'
        )
    return user

@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Wrong username or password.'
        )
    user = UserInDB(**user_dict)
    if not pwd_context.verify(form_data.password, user.hashed_password): 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Wrong username or password.'
        )
    

    token_data = {
        "username": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    }
    encoded_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITH)

    return {"access_token": encoded_token, "token_type": "bearer"}

@app.get('/users/me')
def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/path_parameter/{item_id}", tags=['path parameters'])
def path_parameter(item_id: int):
    return {"path_parameter": item_id}

@app.get('/path_parameter/validations/{item_id}', tags=['path parameters validations'])
def path_parameter_validation(item_id: Annotated[int, Path(title='any titleeeee here', gt=0, le=10)]):
    return {"item_id": item_id}

@app.get('/path_parameter/predefined/values/{model_name}', tags=['path parameters'])
def predefined_parameter(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"choose": "alexnet"}
    elif model_name is ModelName.resnet:
        return {"choose": "resnet"}
    else:
        return {"choose": "lenet"}
    
@app.get('/query_parameters/required', tags=['query parameters'], summary='Query parameters required')
def query_parameters(parameter1: str, parameter2: str):
    return {"parameter1": parameter1, "parameter2": parameter2}

@app.get('/query_parameters/notrequired/', tags=['query parameters'], summary='Query parameters not required')
def query_paramteres_not_required(param1: str| None = None, param2: str|None = None):
    return {"parameter1": param1, "parameter2": param2}

@app.get('/query_parameters/suma/', tags=['query parameters'], summary='Query parameters with default value with integers')
def query_parameters(a: int = 0, b: int = 0):
    return {"result": a + b}

@app.get('/query_parameters/booleans/', tags=['query parameters'])
def query_parameters_booleans(boolean: bool|None=False):
    return {"boolean": boolean}

@app.get('/path_query_body_parameters/{path}')
def path_query_body_parameters(path: str, user: User, query: str):
    return {
        "path": path,
        "user": user,
        "query": query
    }

@app.get('/validations/string', tags=['validations'])
def validations(q: Annotated[str | None, Query(max_length=50, min_length=3)] = None):
    return {"q": q}

@app.get('/validations/integer', tags=['validations'])
def int_validations(q: Annotated[int | None, Query(gt=0)] = None):
    return {"q": q}

@app.get('/ubuntu')
def ubuntu_road():
    return {"os": "ubuntu"}

@app.get("/windows")
def windows_road():
    return {"os": "windows"}

@app.get('/users')
def read_users():
    return {"users": [{"name": "juan"}, {"name": "brayan"}]}

@app.put('/users/{id}')
def update_users(id: int):
    return {"msg": f"user with the id: {id} was updated successfully"}

@app.delete('/users/{id}')
def delete_users(id: int):
    return {"msg": f"user with the id: {id} was deleted successfully"}
