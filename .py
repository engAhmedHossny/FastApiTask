from ast import Raise
from logging import raiseExceptions
from signal import raise_signal
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    text: str = None
    is_done: bool = False

items = []

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

@app.post("/items")
async def create_items(item: Item):
    items.append(item)
    return items

@app.get("/items", response_model=list[Item])
async def list_items(limit: int = 10):
    return items[0:limit]

@app.get("/items/{item_id}", response_model=Item)
async def get_items(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code= 404, detail= f"Item {item_id} not found")
    
