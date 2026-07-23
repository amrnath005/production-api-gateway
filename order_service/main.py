from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Order Service")


class Order(BaseModel):
    product: str
    quantity: int


@app.get("/orders")
def get_orders():
    return {
        "service": "Order Service",
        "orders": [
            {
                "id": 101,
                "product": "Laptop",
                "quantity": 2
            },
            {
                "id": 102,
                "product": "Keyboard",
                "quantity": 5
            }
        ]
    }


@app.post("/orders")
def create_order(order: Order):
    return {
        "message": "Order created successfully",
        "order": order
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }