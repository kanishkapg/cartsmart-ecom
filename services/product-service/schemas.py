from pydantic import BaseModel
from typing import Optional

# Base properties shared across multiple schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

# Schema for creating a product (inherits base, needs nothing extra right now)
class ProductCreate(ProductBase):
    pass

# Schema for returning a product from the API
class ProductResponse(ProductBase):
    id: int

    class Config:
        # Tells Pydantic to read data even if it's an ORM model (SQLAlchemy), not just a dictionary
        from_attributes = True