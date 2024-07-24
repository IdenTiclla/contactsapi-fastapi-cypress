from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from routers import contacts
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import jwt
from jwt.exceptions import InvalidTokenError

TOKEN_EXPIRATION_MINUTES = 1
SECRET_KEY = '9e599617f42ea3f7fbb58f4566d31b72c1970323a68d65cd8fa3258483ecfdb3'
ALGORITH = 'HS256'

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

# fake users db

fake_users_db = {
    "jhondoe": {
        "username": "jhondoe",
        "phone": "77074485",
        "email": "jhondoe@gmail.com",
        "age": 19,
        "disabled": False,
        "hashed_password": "fakehashedsecret1"
    },
    "alice": {
        "username": "alice",
        "phone": "77074159",
        "email": "alice@gmail.com",
        "age": 15,
        "disabled": True,
        "hashed_password": "fakehashedsecret1"
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
            detail='Wrong username or password'
        )
    user = UserInDB(**user_dict)
    if not user.hashed_password == fake_hash_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Wrong username or password'
        )
    

    token_data = {
        "username": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    }
    encoded_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITH)

    return {"token_access": encoded_token, "token_type": "bearer"}

@app.get('/users/me')
def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/name")
def custom_read():
    return {"name": "Iden"}

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
