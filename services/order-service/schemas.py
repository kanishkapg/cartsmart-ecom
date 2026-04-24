from pydantic import BaseModel
from typing import Optional

# Base properties shared across multiple schemas
class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int

# Schema for creating an order (inherits base, needs nothing extra right now)
class OrderCreate(OrderBase):
    pass

# Schema for returning an order from the API
class OrderResponse(OrderBase):
    id: int
    total_price: float

    class Config:
        # Tells Pydantic to read data even if it's an ORM model (SQLAlchemy), not just a dictionary
        from_attributes = True