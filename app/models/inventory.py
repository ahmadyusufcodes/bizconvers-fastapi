from pydantic import BaseModel
from bson import ObjectId
from typing import List, Optional

class Product(BaseModel):
    name: str
    description: str
    price: float
    availability: bool
    image: str
    unit: str
    stock: int
    attributes: dict
    category_id: ObjectId

class Category(BaseModel):
    name: str
    description: str

class OrderItem(BaseModel):
    product_id: ObjectId
    quantity: int
    price: float
    total: float

class Order(BaseModel):
    customer: str
    staff_id: ObjectId
    products: List[OrderItem]
    payment_method: str
    total: float
    status: str
    discount: float
    attributes: dict