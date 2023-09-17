from pydantic import BaseModel
from typing import ForwardRef, List, Optional
from enum import Enum

class OrderItem(BaseModel):
    product_id: str
    variant_id: str
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
    branch_id: str
    items: List[OrderItem]
    total: float
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    delivery_method: DeliveryMethod
    delivery_status: DeliveryStatus
    attributes: dict

class OrderPayment(BaseModel):
    order_id: str
    amount: float
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    attributes: dict

class OrderDelivery(BaseModel):
    order_id: str
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
    order_id: str
    status: OrderStatus
    attributes: dict

class CartItem(BaseModel):
    product_id: str
    variant_id: str
    quantity: int
    attributes: dict

class Cart(BaseModel):
    customer: str
    tag_color: str = "#fff"
    branch_id: str
    items: List[CartItem]
    attributes: dict
