from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from starlette.status import HTTP_400_BAD_REQUEST

from ..models import payments as model
from sqlalchemy.exc import SQLAlchemyError

from ..schemas.payments import PaymentsBase


def create_payment(request: PaymentsBase, db: Session):
    new_payment = model.Payments(
        customer_id = request.customer_id,
        payment_type = request.payment_type,
        transaction_status = request.transaction_status,
        card_info = request.card_info,
        card_date = request.card_date,
        card_pin = request.card_pin,
    )

    try:
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error)

def read_payment(db: Session, payment_id):
    try:
        payment = db.query(model.Payments).filter(model.Payments.id == payment_id).first()
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return payment

def read_all_payments(db: Session):
    try:
        result = db.query(model.Payments).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def update_payment(db: Session, payment_id, request):
    try:
        payment = db.query(model.Payments).filter(model.Payments.id == payment_id)
        if not payment.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found!")
        update_data =request.dict(exclude_unset=True)
        payment.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return payment.first()

def delete_payment(db: Session, payment_id):
    try:
        payment = db.query(model.Payments).filter(model.Payments.id == payment_id)
        if not payment.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found!")
        payment.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)