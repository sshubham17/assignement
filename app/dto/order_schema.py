from pydantic import BaseModel, Field
from typing import List

class OrderItemSchema(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity must be greater than zero")

class OrderCreate(BaseModel):
    products: List[OrderItemSchema]  # List of ordered products

class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str
