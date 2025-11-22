from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models.promotions import Promotion
from ..models.orders import Order
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_item = model.Promotion(
        promo_code=request.promo_code,
        expiration_date=request.expiration_date
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item

def read_all(db: Session):
    try:
        result = db.query(model.Promotion).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.Promotion).filter(model.Promotion.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return item

def update(db: Session, item_id: int, request):
    try:
        item = db.query(model.Promotion).filter(model.Promotion.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")

        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return item.first()

def apply_promo(db: Session, order_id: int, promo_code: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")
    promo = db.query(Promotion).filter(Promotion.promo_code == promo_code).first()
    if not promo:
        raise HTTPException(404, "Promo code not found")
    if promo.expiration_date < datetime.now():
        raise HTTPException(400, "Promo code has expired")
    order.promotion_id = promo.id
    db.commit()
    db.refresh(order)

    return order

def delete(db: Session, item_id: int):
    try:
        item = db.query(model.Promotion).filter(model.Promotion.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")

        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return Response(status_code=status.HTTP_204_NO_CONTENT)