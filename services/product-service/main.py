from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models
import schemas
import crud
import httpx
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Service")

USER_SERVICE_URL = "http://user-service:8001"

@app.post("/products/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # We make a synchronous GET request to the User Service to check if the owner (user) exists before creating the product
    try:
        # Create a client that explicitly ignores system proxy environment variables
        with httpx.Client(trust_env=False) as client:
            response = client.get(
                f"{USER_SERVICE_URL}/users/{product.owner_id}"
            )
        # If the User Service returns a 404 Not Found, we block the product creation
        if response.status_code == 404:
            raise HTTPException(status_code=400, detail="Owner(User) does not exist")
        response.raise_for_status()  # Raise an error for any other bad status codes
    except httpx.HTTPError:
        # This catches network failures (e.g., you forgot to start the User Service)
        raise HTTPException(status_code=503, detail="User Service is unavailable.")

    return crud.create_product(db=db, product=product)

@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product