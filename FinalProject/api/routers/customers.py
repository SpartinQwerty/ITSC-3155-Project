from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..controllers import customers as controller
from ..schemas import customers as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Customers"],
    prefix="/customers"
)

@router.post("/", response_model=schema.Customer)
def create_customer(customer: schema.CustomerCreate, db: Session = Depends(get_db)):
    return controller.create_customer(request=customer, db=db)

@router.get("/", response_model=schema.Customer)
def read_all_customers(db: Session = Depends(get_db)):
    return controller.read_all_customers(db=db)

@router.get("/{customer_id}", response_model=schema.Customer)
def read_one_customer(customer_id: int, db: Session = Depends(get_db)):
    return controller.read_one_customer(db=db, customer_id=customer_id)

@router.put("/{customer_id}", response_model=schema.Customer)
def update_customer(customer_id: int, customer: schema.CustomerUpdate, db: Session = Depends(get_db)):
    return controller.update_customer(db=db, customer_id=customer_id, request=customer)

@router.delete("/{customer_id}", response_model=schema.Customer)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return controller.delete_customer(db=db, customer_id=customer_id)