from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from routers import contacts

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated

# oauth2 scheme

oauth2_scheme = OAuth2PasswordBearer('login')

app = FastAPI()

app.include_router(contacts.router)

# Model
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserInDB(User):
    hashed_password: str

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Inactive user'
        )
    return current_user

def fake_hash_password(password):
    return 'fakehashed' + password

@app.post('/login')
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password.'
        )
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password.'
        )
    return {"access_token": user.username, "token_type": "bearer"}

@app.get('/users/me')
def users_me(user: Annotated[User, Depends(get_current_active_user)]):
    return user

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
