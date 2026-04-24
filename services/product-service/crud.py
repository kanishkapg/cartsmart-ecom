from sqlalchemy.orm import Session
import models
import schemas

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    # Convert Pydantic schema to SQLAlchemy model
    db_product = models.Product(
        name = product.name,
        description = product.description,
        price = product.price,
        owner_id = product.owner_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)  # Refresh to get the generated ID
    return db_product