from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100), ForeignKey("customers.name"), nullable=False)
    payment_type = Column(String(100), nullable=False)
    transaction_status = Column(String(100), nullable=False)
    card_info = Column(Integer(), nullable=True)
    card_date = Column(String(10), nullable=True)
    card_pin = Column(Integer(), nullable=True)

    #relationships
    customers = relationship("Customers", back_populates="payments")

