from fastapi import FastAPI
from pydantic import BaseModel
from routers import contacts


app = FastAPI()

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
