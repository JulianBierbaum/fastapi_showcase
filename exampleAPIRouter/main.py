from fastapi import FastAPI
from routers import users, items, orders

app = FastAPI()

# Include routers with prefix to organize the API
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
