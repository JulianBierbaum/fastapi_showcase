from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_orders():
    return {"message": "List of orders"}

@router.get("/{order_id}")
def get_order(order_id: int):
    return {"order_id": order_id, "message": "Order details"}
