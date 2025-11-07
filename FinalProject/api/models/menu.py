from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dish = Column(String)
    ingredients = Column(String)
    price = Column(DECIMAL)
    calories = Column(DECIMAL)
    category = Column(String)
    description = Column(String(300))

    # Relationships
    #Will implement in part 3