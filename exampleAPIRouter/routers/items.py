from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_items():
    return {"message": "List of items"}

@router.get("/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "message": "Item details"}
