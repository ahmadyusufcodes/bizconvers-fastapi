from pydantic import BaseModel
from bson import ObjectId
from typing import List, Optional
from enum import Enum

class Product(BaseModel):
    name: str
    description: str
    images: List[str]
    unit: str
    category_id: ObjectId
    attributes: dict

class ProductVariant(BaseModel):
    product_id: ObjectId
    name: str
    description: str
    images: List[str]
    unit: str
    attributes: dict

class ProductInBranch(BaseModel):
    product_id: ObjectId
    branch_id: ObjectId
    price: float
    quantity: int
    attributes: dict
    in_stock: bool

class ProductVariantInBranch(BaseModel):
    product_id: ObjectId
    variant_id: ObjectId
    branch_id: ObjectId
    price: float
    quantity: int
    attributes: dict
    in_stock: bool

class Category(BaseModel):
    name: str
    description: str
    company_id: ObjectId
    attributes: dict

class OrderItem(BaseModel):
    product_id: ObjectId
    variant_id: ObjectId
    quantity: int
    attributes: dict

class PaymentMethod(str, Enum):
    CASH = "CASH"
    MOBILE_MONEY = "MOBILE_MONEY"
    CARD = "CARD"

class PaymentStatus(str, Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"

class DeliveryMethod(str, Enum):
    PICKUP = "PICKUP"
    DELIVERY = "DELIVERY"

class DeliveryStatus(str, Enum):
    DELIVERED = "DELIVERED"
    UNDELIVERED = "UNDELIVERED"

class Order(BaseModel):
    customer: str
    branch_id: ObjectId
    items: List[OrderItem]
    total: float
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    delivery_method: DeliveryMethod
    delivery_status: DeliveryStatus
    attributes: dict

class OrderPayment(BaseModel):
    order_id: ObjectId
    amount: float
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    attributes: dict

class OrderDelivery(BaseModel):
    order_id: ObjectId
    amount: float
    delivery_method: DeliveryMethod
    delivery_status: DeliveryStatus
    attributes: dict

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class OrderStatusUpdate(BaseModel):
    order_id: ObjectId
    status: OrderStatus
    attributes: dict

class CartItem(BaseModel):
    product_id: ObjectId
    variant_id: ObjectId
    quantity: int
    attributes: dict

class Cart(BaseModel):
    customer: str
    tag_color: str = "#fff"
    branch_id: ObjectId
    items: List[CartItem]
    attributes: dict
