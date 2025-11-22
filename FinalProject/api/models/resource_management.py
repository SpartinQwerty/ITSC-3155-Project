from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class ResourceManagement(Base):
    __tablename__ = "resources_management"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ingredient = Column(String(100), unique=True, nullable=False)
    amount = Column(Integer, nullable=False, default=0)
    unit = Column(String(50), nullable=False)