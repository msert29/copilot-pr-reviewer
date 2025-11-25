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


# VIOLATION: Not following DTO naming convention
# Should be: RestAPICreateProductRequestDTO
class ProductCreate(BaseModel):
    name: str
    price: Decimal
    description: Optional[str]


# VIOLATION: Not following DTO naming convention
# Should be: RestAPIProductResponseDTO or RestAPIProductDTO
class Product(BaseModel):
    id: uuid.UUID
    name: str
    price: Decimal
    description: Optional[str] = None


# VIOLATION: Not following DTO naming convention
# Should be: RestAPIListProductsResponseDTO
class ProductList(BaseModel):
    # VIOLATION: Missing total_count field for pagination
    # Should have: total_count: int
    products: List[Product]


# VIOLATION: Abbreviated variable names (prod, prods, p)
# VIOLATION: Not using HTTPStatus enum
@app.get("/products")
def get_products(
    # VIOLATION: Should use page and page_size naming
    pg: int = Query(1, alias="page"),
    limit: int = Query(10, alias="page_size")
):
    prods = []
    
    # VIOLATION: Abbreviated loop variable 'p'
    for p in range(5):
        prod = Product(
            id=uuid.uuid4(),
            name=f"Product {p}",
            price=Decimal("10.99"),
            description="Test product"
        )
        prods.append(prod)
    
    # VIOLATION: Not using proper pagination response structure
    # VIOLATION: Not using HTTPStatus enum for status code
    return {"products": prods, "count": len(prods)}


# VIOLATION: Not following DTO naming convention
# Should be: RestAPICreateProductResponseDTO
class CreateResponse(BaseModel):
    message: str
    product_id: uuid.UUID


# VIOLATION: Abbreviated variable name 'prod'
# VIOLATION: Not using HTTPStatus enum
# VIOLATION: Error response doesn't use standardized structure with 'detail' and 'code'
@app.post("/products", status_code=201)
def create_product(prod: ProductCreate):
    if not prod.name:
        # VIOLATION: Not using proper error response structure
        # Should use: detail, code, and HTTPStatus
        raise HTTPException(status_code=400, detail="Name required")
    
    # VIOLATION: Abbreviated variable name 'new_prod'
    new_prod = Product(
        id=uuid.uuid4(),
        name=prod.name,
        price=prod.price,
        description=prod.description
    )
    
    # VIOLATION: Not using HTTPStatus enum
    return CreateResponse(
        message="Product created",
        product_id=new_prod.id
    )


# VIOLATION: Abbreviated variable names (u, usr)
# VIOLATION: Not following DTO naming conventions
class User(BaseModel):
    id: uuid.UUID
    name: str
    email: str


# VIOLATION: Multiple abbreviated variable names
# VIOLATION: Not using HTTPStatus enum
@app.get("/users/{user_id}")
def get_user(user_id: uuid.UUID):
    # VIOLATION: Abbreviated variable name 'u'
    u = User(
        id=user_id,
        name="John Doe",
        email="john@example.com"
    )
    
    return u


# VIOLATION: Abbreviated variable names in loop
# VIOLATION: Missing type hints
# VIOLATION: Not following DTO naming conventions
@app.get("/orders")
def list_orders(status=None):
    orders = []
    
    # VIOLATION: Abbreviated loop variable 'o'
    for o in range(3):
        order = {
            "id": str(uuid.uuid4()),
            "status": "pending",
            "total": 100.00
        }
        orders.append(order)
    
    return {"orders": orders}


# VIOLATION: Untyped function decorator (would disable mypy)
def cache_response(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


# VIOLATION: Using untyped decorator
@app.get("/cached-data")
@cache_response
def get_cached_data():
    return {"data": "cached"}


# VIOLATION: Not following DTO naming convention
# Should be: RestAPIUpdateInventoryRequestDTO
class InventoryUpdate(BaseModel):
    quantity: int
    location: str


# VIOLATION: Not following DTO naming convention
# Should be: RestAPIUpdateInventoryResponseDTO
class InventoryResponse(BaseModel):
    success: bool
    # VIOLATION: Abbreviated field name 'qty'
    qty: int


# VIOLATION: Abbreviated parameter name 'inv_id'
# VIOLATION: Abbreviated variable names throughout
# VIOLATION: Not using HTTPStatus enum
@app.put("/inventory/{inv_id}")
def update_inventory(inv_id: uuid.UUID, data: InventoryUpdate):
    # VIOLATION: Abbreviated variable name 'curr_qty'
    curr_qty = 50
    
    # VIOLATION: Abbreviated variable name 'new_qty'
    new_qty = curr_qty + data.quantity
    
    # VIOLATION: Abbreviated variable name 'resp'
    resp = InventoryResponse(
        success=True,
        qty=new_qty
    )
    
    return resp


# VIOLATION: Missing pagination structure (total_count, results)
# VIOLATION: Abbreviated variable names
@app.get("/categories")
def get_categories(
    page: int = 1,
    page_size: int = 10
):
    cats = []
    
    # VIOLATION: Abbreviated loop variable 'c'
    for c in range(page_size):
        cat = {
            "id": str(uuid.uuid4()),
            "name": f"Category {c}"
        }
        cats.append(cat)
    
    # VIOLATION: Missing total_count field
    # Should return: {"total_count": int, "results": List[...]}
    return {"categories": cats, "page": page}


# VIOLATION: Comment doesn't follow PY3.X format for future upgrades
# Should be: # PY3.11: use match/case statement here
def process_status(status_code: int):
    # TODO: use match statement when we upgrade Python
    if status_code == 200:
        return "OK"
    elif status_code == 404:
        return "Not Found"
    else:
        return "Unknown"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)