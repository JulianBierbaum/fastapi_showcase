from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from typing import List

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

# Globale Liste zur Speicherung von Items
item_list: List[Item] = []

# GET-Request für Modelle
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

# POST-Request zum Hinzufügen eines Items
@app.post("/add_items/")
async def create_item(item: Item):
    item_list.append(item)
    return {"message": "Item added successfully", "item": item}

# GET-Request zum Abrufen eines Items basierend auf Index
@app.get("/get_items/")
async def get_item(index: int):
    # Validierung des Index, um Abstürze zu verhindern
    if index < 0 or index >= len(item_list):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": item_list[index]}

# Endpunkt zum Abrufen aller Items
@app.get("/all_items/")
async def get_all_items():
    return {"items": item_list}
