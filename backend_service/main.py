import os

from fastapi import FastAPI
from pydantic import BaseModel
from app.routers.metrics import router as metrics_router

app = FastAPI(title="User Service")

# This identifies the running instance.
# If INSTANCE_NAME is not provided, it defaults to "Unknown".
INSTANCE_NAME = os.getenv("INSTANCE_NAME", "Unknown")
app.include_router(metrics_router)


class User(BaseModel):
    username: str
    email: str
    age: int


@app.get("/users")
def get_users():
    return {
        "service": "User Service",
        "instance": INSTANCE_NAME,
        "users": [
            {
                "id": 1,
                "name": "Amarnath"
            },
            {
                "id": 2,
                "name": "Rahul"
            }
        ]
    }


@app.post("/users")
def create_user(user: User):
    return {
        "instance": INSTANCE_NAME,
        "message": "User created in Backend Service",
        "user": user
    }


@app.get("/health")
def health():
    return {
        "instance": INSTANCE_NAME,
        "status": "healthy"
    }