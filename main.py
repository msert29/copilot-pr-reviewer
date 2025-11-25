"""
Main FastAPI application with intentional guideline violations
"""
import uuid
from decimal import Decimal
from typing import Optional, List
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel


app = FastAPI()


class ProductCreate(BaseModel):
    name: str
    price: Decimal
    description: Optional[str]

class Product(BaseModel):
    id: uuid.UUID
    name: str
    price: Decimal
    description: Optional[str] = None

class ProductList(BaseModel):

    products: List[Product]

@app.get("/products")
def get_products(
    pg: int = Query(1, alias="page"),
    limit: int = Query(10, alias="page_size")
):
    prods = []
    
    for p in range(5):
        prod = Product(
            id=uuid.uuid4(),
            name=f"Product {p}",
            price=Decimal("10.99"),
            description="Test product"
        )
        prods.append(prod)
    
    return {"products": prods, "count": len(prods)}


class CreateResponse(BaseModel):
    message: str
    product_id: uuid.UUID



@app.post("/products", status_code=201)
def create_product(prod: ProductCreate):
    if not prod.name:
        raise HTTPException(status_code=400, detail="Name required")
    
    new_prod = Product(
        id=uuid.uuid4(),
        name=prod.name,
        price=prod.price,
        description=prod.description
    )
    
    return CreateResponse(
        message="Product created",
        product_id=new_prod.id
    )


class User(BaseModel):
    id: uuid.UUID
    name: str
    email: str


@app.get("/users/{user_id}")
def get_user(user_id: uuid.UUID):
    u = User(
        id=user_id,
        name="John Doe",
        email="john@example.com"
    )
    
    return u


@app.get("/orders")
def list_orders(status=None):
    orders = []
    
    for o in range(3):
        order = {
            "id": str(uuid.uuid4()),
            "status": "pending",
            "total": 100.00
        }
        orders.append(order)
    
    return {"orders": orders}


def cache_response(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@app.get("/cached-data")
@cache_response
def get_cached_data():
    return {"data": "cached"}


class InventoryUpdate(BaseModel):
    quantity: int
    location: str


class InventoryResponse(BaseModel):
    success: bool
    qty: int


@app.put("/inventory/{inv_id}")
def update_inventory(inv_id: uuid.UUID, data: InventoryUpdate):
    curr_qty = 50
    
    new_qty = curr_qty + data.quantity
    
    resp = InventoryResponse(
        success=True,
        qty=new_qty
    )
    
    return resp

@app.get("/categories")
def get_categories(
    page: int = 1,
    page_size: int = 10
):
    cats = []
    
    for c in range(page_size):
        cat = {
            "id": str(uuid.uuid4()),
            "name": f"Category {c}"
        }
        cats.append(cat)
    
    return {"categories": cats, "page": page}


def process_status(status_code: int):
    if status_code == 200:
        return "OK"
    elif status_code == 404:
        return "Not Found"
    else:
        return "Unknown"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)