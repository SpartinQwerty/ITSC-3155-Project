from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import orders, customers, reviews as model
from sqlalchemy.exc import SQLAlchemyError




def create(db: Session, request):
    # Check if customer exists
    customer = db.query(customers.Customer).filter(
        customers.Customer.id == request.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {request.customer_id} not found"
        )

    # Check if order exists
    order = db.query(orders.Order).filter(
        orders.Order.id == request.order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {request.order_id} not found"
        )

    new_item = model.Review(
        customer_id=request.customer_id,
        order_id=request.order_id,
        review_text=request.review_text,
        score=request.score
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.dict['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item




def read_all(db: Session):
   try:
       result = db.query(model.Review).all()
   except SQLAlchemyError as e:
       error = str(e.__dict__['orig'])
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
   return result




def read_one(db: Session, item_id):
   try:
       item = db.query(model.Review).filter(model.Review.id == item_id).first()
       if not item:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
   except SQLAlchemyError as e:
       error = str(e.__dict__['orig'])
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
   return item




def update(db: Session, item_id, request):
   try:
       item = db.query(model.Review).filter(model.Review.id == item_id)
       if not item.first():
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
       update_data = request.dict(exclude_unset=True)
       item.update(update_data, synchronize_session=False)
       db.commit()
   except SQLAlchemyError as e:
       error = str(e.__dict__['orig'])
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
   return item.first()




def delete(db: Session, item_id):
   try:
       item = db.query(model.Review).filter(model.Review.id == item_id)
       if not item.first():
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
       item.delete(synchronize_session=False)
       db.commit()
   except SQLAlchemyError as e:
       error = str(e.__dict__['orig'])
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
   return Response(status_code=status.HTTP_204_NO_CONTENT)




# Bonus functions for User Story 7 - feedback analysis
def read_by_customer(db: Session, customer_id: int):
   try:
       result = db.query(model.Review).filter(model.Review.customer_id == customer_id).all()
   except SQLAlchemyError as e:
       error = str(e.__dict__['orig'])
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
   return result




def read_by_order(db: Session, order_id: int):
   try:
       result = db.query(model.Review).filter(model.Review.order_id == order_id).all()
   except SQLAlchemyError as e:
       error = str(e.__dict__['orig'])
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
   return result




def get_average_rating(db: Session):
   try:
       from sqlalchemy import func
       avg_score = db.query(func.avg(model.Review.score)).scalar()
       total_reviews = db.query(func.count(model.Review.id)).scalar()
       return {
           "average_rating": float(avg_score) if avg_score else 0.0,
           "total_reviews": total_reviews
       }
   except SQLAlchemyError as e:
       error = str(e.__dict__['orig'])
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)