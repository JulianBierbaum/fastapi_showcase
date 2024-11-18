from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from typing import List

# This class defines a set of predefined model names using Python's Enum class.
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# Pydantic's BaseModel is used to define the structure of an object and automatically validate the incoming data.
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# creating instance of fastapi
app = FastAPI()

# global list for storing added Items
item_list: List[Item] = []

# GET-Request for models, using the parameter you can get information about a specific model 
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

# POST-Request for items, this allows clients to send an Item object in the request body which then gets added to the item list
@app.post("/add_items/")
async def create_item(item: Item):
    item_list.append(item)
    return {"message": "Item added successfully", "item": item}

# GET-Request for items, this endpoint accepts a query parameter 'index' to fetch an item by its position in item_list.
@app.get("/get_items/")
async def get_item(index: int):
    # validating index, returning error if invalid
    if index < 0 or index >= len(item_list):
        raise HTTPException(status_code=400, detail="Invalid index provided, item not found")
    return {"item": item_list[index]}

# This endpoint returns all the items stored in item_list.
@app.get("/all_items/")
async def get_all_items():
    return {"items": item_list}
