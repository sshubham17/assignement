
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    description: str = Field(..., description="Product description")
    price: float = Field(..., gt=0, description="Price must be greater than zero")
    stock: int = Field(..., ge=0, description="Stock cannot be negative")

class ProductResponse(ProductCreate):
    id: int = Field(..., description="Unique product ID")
