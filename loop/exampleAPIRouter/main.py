from fastapi import FastAPI, HTTPException
from routers import users, projects, FastApiAuthorization

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(FastApiAuthorization.router, prefix="/security", tags=["Security"])
