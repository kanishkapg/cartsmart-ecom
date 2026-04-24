from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models
import schemas
import crud
import httpx
import json
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service")

PRODUCT_SERVICE_URL = "http://127.0.0.1:8000"
USER_SERVICE_URL = "http://127.0.0.1:8001"

@app.post("/orders/", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    #Validate User exists
    try:
        user_response = httpx.get(f"{USER_SERVICE_URL}/users/{order.user_id}")

        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="User is not found")
        
        user_response.raise_for_status()
    
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"User service unavailable: {str(e)}")
    
    # Validate Product exists and get price
    try:
        product_response = httpx.get(f"{PRODUCT_SERVICE_URL}/products/{order.product_id}")

        if product_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Product is not found")
        else:
            product_data = product_response.json()
            unit_price = product_data["price"]

        product_response.raise_for_status()
    
    except httpx.HTTPError:
        raise HTTPException(status_code=503, detail=f"Product service unavailable")
    
    total_price = unit_price * order.quantity
    
    return crud.create_order(db=db, order=order, total_price=total_price)

