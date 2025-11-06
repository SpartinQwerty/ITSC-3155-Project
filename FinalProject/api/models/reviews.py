from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    review_text = Column(String(500), nullable=True)
    score = Column(DECIMAL(2, 1), nullable=False)
    review_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))

    # Relationships
    customer = relationship("Customer", back_populates="reviews")
    order = relationship("Order", back_populates="reviews")