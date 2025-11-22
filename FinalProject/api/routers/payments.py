from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..controllers import payments as controller
from ..schemas import payments as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Payments"],
    prefix="/payments"
)

@router.post("/", response_model=schema.Payments)
def create_payment(payment: schema.PaymentsCreate, db: Session = Depends(get_db)):
    return controller.create_payment(request=payment, db=db)

@router.get("/", response_model=list[schema.Payments])
def read_all_payments(db: Session = Depends(get_db)):
    return controller.read_all_payments(db=db)

@router.get("/{payment_id}", response_model=schema.Payments)
def read_one_payment(payment_id: int, db: Session = Depends(get_db)):
    return controller.read_payment(db=db, payment_id=payment_id)

@router.put("/{payment_id}", response_model=schema.Payments)
def update_payment(
    payment_id: int,
    payment: schema.PaymentsUpdate,
    db: Session = Depends(get_db)
):
    return controller.update_payment(db=db, payment_id=payment_id, request=payment)

@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    return controller.delete_payment(db=db, payment_id=payment_id)
