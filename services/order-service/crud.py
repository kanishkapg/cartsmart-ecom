from sqlalchemy.orm import Session
import models
import schemas

def create_order(db: Session, order: schemas.OrderCreate, total_price: float):
    # Convert Pydantic schema to SQLAlchemy model
    db_order = models.Order(
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)  # Refresh to get the generated ID
    return db_order