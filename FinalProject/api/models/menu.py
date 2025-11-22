from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dish = Column(String(100))
    ingredients = Column(String(500))
    price = Column(DECIMAL(10, 2))
    calories = Column(DECIMAL(10, 2))
    category = Column(String(50))
    description = Column(String(300))
    is_vegetarian = Column(Boolean, default=False)
