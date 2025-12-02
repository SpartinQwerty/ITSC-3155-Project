from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import orders as model
from sqlalchemy.exc import SQLAlchemyError
from ..models.menu import Menu
from ..models.order_details import OrderDetail


def create(db: Session, request):

    # Calculate total price BEFORE creating order
    total_price = 0

    for detail in request.order_details:
        menu_item = db.query(Menu).filter(Menu.id == detail.dish_id).first()
        if not menu_item:
            raise HTTPException(
                status_code=400,
                detail=f"Menu item {detail.dish_id} not found"
            )
        total_price += float(menu_item.price) * detail.amount

    # Create the order
    new_order = model.Order(
        customer_id=request.customer_id,
        description=request.description,
        total_price=total_price
    )

    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Create order details AFTER order id exists
        for detail in request.order_details:
            od = OrderDetail(
                order_id=new_order.id,
                dish_id=detail.dish_id,
                amount=detail.amount
            )
            db.add(od)

        db.commit()
        db.refresh(new_order)

    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_order


def read_all(db: Session):
    try:
        return db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found")
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def update(db: Session, item_id: int, request):
    # Get the order
    order = db.query(model.Order).filter(model.Order.id == item_id).first()
    if not order:
        raise HTTPException(404, "Order not found")

    # Convert request to dict excluding unset fields
    update_data = request.dict(exclude_unset=True)

    if "order_details" in update_data and update_data["order_details"] is not None:
        # Remove old order details
        db.query(OrderDetail).filter(OrderDetail.order_id == item_id).delete()

        # Recalculate total_price
        new_total = 0
        for detail in update_data["order_details"]:
            # Access dict keys (not attributes)
            dish_id = detail["dish_id"]
            amount = detail["amount"]

            # Get menu item price
            menu_item = db.query(Menu).filter(Menu.id == dish_id).first()
            if not menu_item:
                raise HTTPException(400, f"Menu item {dish_id} not found")

            # Create new OrderDetail row
            od = OrderDetail(
                order_id=item_id,
                dish_id=dish_id,
                amount=amount
            )
            db.add(od)

            # Add to total price
            new_total += float(menu_item.price) * amount

        order.total_price = new_total

    if "customer_id" in update_data:
        order.customer_id = update_data["customer_id"]

    if "description" in update_data:
        order.description = update_data["description"]

    db.commit()
    db.refresh(order)
    return order


def delete(db: Session, item_id: int):
    try:
        order = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found!")

        # Delete associated order_details
        db.query(OrderDetail).filter(OrderDetail.order_id == item_id).delete()

        # Delete the order
        db.delete(order)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=400, detail=error)

    return Response(status_code=204)