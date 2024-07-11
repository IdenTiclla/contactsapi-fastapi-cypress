from typing import Union

from fastapi import FastAPI

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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
