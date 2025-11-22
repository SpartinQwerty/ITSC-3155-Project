from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from fastapi import HTTPException, status
from ..models import order_details as order_detail_model
from ..models import orders as order_model
from ..models import sandwiches as sandwich_model
from ..models import reviews as review_model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date


def get_popular_dishes(db: Session, limit: int = 10):
    """Get the most popular dishes based on order frequency"""
    try:
        # Query to get sandwich name, total orders, and total quantity sold
        popular = db.query(
            sandwich_model.Sandwich.id,
            sandwich_model.Sandwich.sandwich_name,
            func.count(order_detail_model.OrderDetail.id).label('times_ordered'),
            func.sum(order_detail_model.OrderDetail.amount).label('total_quantity')
        ).join(
            order_detail_model.OrderDetail,
            sandwich_model.Sandwich.id == order_detail_model.OrderDetail.sandwich_id
        ).group_by(
            sandwich_model.Sandwich.id
        ).order_by(
            func.count(order_detail_model.OrderDetail.id).desc()
        ).limit(limit).all()

        result = []
        for item in popular:
            result.append({
                "sandwich_id": item.id,
                "sandwich_name": item.sandwich_name,
                "times_ordered": item.times_ordered,
                "total_quantity_sold": int(item.total_quantity)
            })

        return result
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def get_unpopular_dishes(db: Session, limit: int = 10):
    """Get the least popular dishes based on order frequency"""
    try:
        # Get all sandwiches with their order counts
        unpopular = db.query(
            sandwich_model.Sandwich.id,
            sandwich_model.Sandwich.sandwich_name,
            func.count(order_detail_model.OrderDetail.id).label('times_ordered'),
            func.sum(order_detail_model.OrderDetail.amount).label('total_quantity')
        ).outerjoin(
            order_detail_model.OrderDetail,
            sandwich_model.Sandwich.id == order_detail_model.OrderDetail.sandwich_id
        ).group_by(
            sandwich_model.Sandwich.id
        ).order_by(
            func.count(order_detail_model.OrderDetail.id).asc()
        ).limit(limit).all()

        result = []
        for item in unpopular:
            result.append({
                "sandwich_id": item.id,
                "sandwich_name": item.sandwich_name,
                "times_ordered": item.times_ordered,
                "total_quantity_sold": int(item.total_quantity) if item.total_quantity else 0
            })

        return result
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def get_dishes_with_complaints(db: Session, min_rating: float = 3.0):
    """Get dishes that have received poor reviews"""
    try:
        # Get sandwiches with low average ratings
        dishes_with_complaints = db.query(
            sandwich_model.Sandwich.id,
            sandwich_model.Sandwich.sandwich_name,
            func.avg(review_model.Review.score).label('avg_rating'),
            func.count(review_model.Review.id).label('review_count')
        ).join(
            order_detail_model.OrderDetail,
            sandwich_model.Sandwich.id == order_detail_model.OrderDetail.sandwich_id
        ).join(
            order_model.Order,
            order_detail_model.OrderDetail.order_id == order_model.Order.id
        ).join(
            review_model.Review,
            order_model.Order.id == review_model.Review.order_id
        ).group_by(
            sandwich_model.Sandwich.id
        ).having(
            func.avg(review_model.Review.score) < min_rating
        ).order_by(
            func.avg(review_model.Review.score).asc()
        ).all()

        result = []
        for item in dishes_with_complaints:
            result.append({
                "sandwich_id": item.id,
                "sandwich_name": item.sandwich_name,
                "average_rating": float(item.avg_rating),
                "review_count": item.review_count
            })

        return result
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def get_daily_revenue(db: Session, target_date: date):
    """Calculate total revenue for a specific date"""
    try:
        # Get all orders from the target date
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())

        # Calculate revenue by joining orders, order_details, and sandwiches
        revenue = db.query(
            func.sum(
                order_detail_model.OrderDetail.amount * sandwich_model.Sandwich.price
            ).label('total_revenue')
        ).join(
            order_model.Order,
            order_detail_model.OrderDetail.order_id == order_model.Order.id
        ).join(
            sandwich_model.Sandwich,
            order_detail_model.OrderDetail.sandwich_id == sandwich_model.Sandwich.id
        ).filter(
            and_(
                order_model.Order.order_date >= start_datetime,
                order_model.Order.order_date <= end_datetime
            )
        ).scalar()

        return {
            "date": str(target_date),
            "total_revenue": float(revenue) if revenue else 0.0
        }
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def get_orders_by_date_range(db: Session, start_date: date, end_date: date):
    """Get all orders within a specific date range"""
    try:
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        orders = db.query(order_model.Order).filter(
            and_(
                order_model.Order.order_date >= start_datetime,
                order_model.Order.order_date <= end_datetime
            )
        ).all()

        return orders
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def get_revenue_by_date_range(db: Session, start_date: date, end_date: date):
    """Calculate total revenue within a date range"""
    try:
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        revenue = db.query(
            func.sum(
                order_detail_model.OrderDetail.amount * sandwich_model.Sandwich.price
            ).label('total_revenue'),
            func.count(order_model.Order.id.distinct()).label('total_orders')
        ).join(
            order_model.Order,
            order_detail_model.OrderDetail.order_id == order_model.Order.id
        ).join(
            sandwich_model.Sandwich,
            order_detail_model.OrderDetail.sandwich_id == sandwich_model.Sandwich.id
        ).filter(
            and_(
                order_model.Order.order_date >= start_datetime,
                order_model.Order.order_date <= end_datetime
            )
        ).first()

        return {
            "start_date": str(start_date),
            "end_date": str(end_date),
            "total_revenue": float(revenue.total_revenue) if revenue.total_revenue else 0.0,
            "total_orders": revenue.total_orders if revenue.total_orders else 0
        }
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)