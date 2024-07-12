from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Contact(BaseModel):
    name: str
    last_name: str
    age: int
    phone_number: int


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
