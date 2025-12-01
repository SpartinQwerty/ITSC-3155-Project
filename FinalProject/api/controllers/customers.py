from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from ..models import customers as model
from ..models.orders import Order
from ..schemas.customers import CustomerBase
from sqlalchemy.exc import SQLAlchemyError

def create_customer(db: Session, request: CustomerBase):
    new_customer = model.Customer(
        name=request.name,
        email=request.email,
        phone_number=request.phone_number,
        address=request.address,
    )

    try:
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error)

def read_one_customer(db: Session,customer_id):
    try:
        customer = db.query(model.Customer).filter(model.Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return customer

def read_all_customers(db: Session):
    try:
        result = db.query(model.Customer).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def update_customer(db: Session, customer_id, request):
    try:
        customer = db.query(model.Customer).filter(model.Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found!")
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(customer, key, value)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return customer

def delete_customer(db: Session, customer_id):
    try:
        customer = db.query(model.Customer).filter(model.Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found!")
        orders = db.query(Order).filter(Order.customer_id == customer_id).all()
        for order in orders:
            db.delete(order)

        db.delete(customer)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
