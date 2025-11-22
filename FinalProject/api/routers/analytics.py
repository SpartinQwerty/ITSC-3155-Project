# Save as: api/routers/analytics.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..controllers import analytics as controller
from ..schemas import orders as order_schema
from ..dependencies.database import get_db
from datetime import date

router = APIRouter(
    tags=['Analytics'],
    prefix="/analytics"
)


@router.get("/popular-dishes")
def get_popular_dishes(limit: int = Query(10, description="Number of top dishes to return"),
                       db: Session = Depends(get_db)):
    """
    Get the most popular dishes based on order frequency.
    Helps answer: "What items are customers ordering most?"
    """
    return controller.get_popular_dishes(db, limit=limit)


@router.get("/unpopular-dishes")
def get_unpopular_dishes(limit: int = Query(10, description="Number of least popular dishes to return"),
                         db: Session = Depends(get_db)):
    """
    Get the least popular dishes.
    Helps answer: "How can I identify dishes that are less popular?"
    """
    return controller.get_unpopular_dishes(db, limit=limit)


@router.get("/dishes-with-complaints")
def get_dishes_with_complaints(min_rating: float = Query(3.0, description="Show dishes rated below this score"),
                               db: Session = Depends(get_db)):
    """
    Get dishes that have received poor reviews.
    Helps answer: "How can I identify dishes that have received complaints?"
    """
    return controller.get_dishes_with_complaints(db, min_rating=min_rating)


@router.get("/daily-revenue")
def get_daily_revenue(target_date: date = Query(..., description="Date in YYYY-MM-DD format"),
                      db: Session = Depends(get_db)):
    """
    Get total revenue for a specific date.
    Helps answer: "How can I determine the total revenue generated from food sales on any given day?"

    Example: /analytics/daily-revenue?target_date=2024-11-17
    """
    return controller.get_daily_revenue(db, target_date=target_date)


@router.get("/orders-by-date-range", response_model=list[order_schema.Order])
def get_orders_by_date_range(start_date: date = Query(..., description="Start date in YYYY-MM-DD format"),
                             end_date: date = Query(..., description="End date in YYYY-MM-DD format"),
                             db: Session = Depends(get_db)):
    """
    Get all orders within a specific date range.
    Helps answer: "Is there a way to view the list of orders within a specific date range?"

    Example: /analytics/orders-by-date-range?start_date=2024-11-01&end_date=2024-11-30
    """
    return controller.get_orders_by_date_range(db, start_date=start_date, end_date=end_date)


@router.get("/revenue-by-date-range")
def get_revenue_by_date_range(start_date: date = Query(..., description="Start date in YYYY-MM-DD format"),
                              end_date: date = Query(..., description="End date in YYYY-MM-DD format"),
                              db: Session = Depends(get_db)):
    """
    Get total revenue and order count within a date range.
    Provides a summary of business performance over time.

    Example: /analytics/revenue-by-date-range?start_date=2024-11-01&end_date=2024-11-30
    """
    return controller.get_revenue_by_date_range(db, start_date=start_date, end_date=end_date)