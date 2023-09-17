from pydantic import BaseModel
from typing import ForwardRef, List, Optional
from enum import Enum

class Category(BaseModel):
    name: str
    description: str = ""
    company_id: str = ""
    attributes: dict = {}


class Product(BaseModel):
    name: str
    description: str
    images: List[str]
    unit: str
    category_id: str
    attributes: dict

class ProductVariant(BaseModel):
    product_id: str
    name: str
    description: str
    images: List[str]
    unit: str
    attributes: dict

class ProductInBranch(BaseModel):
    product_id: str
    branch_id: str
    price: float
    quantity: int
    attributes: dict
    in_stock: bool

class ProductVariantInBranch(BaseModel):
    product_id: str
    variant_id: str
    branch_id: str
    price: float
    quantity: int
    attributes: dict
    in_stock: bool

