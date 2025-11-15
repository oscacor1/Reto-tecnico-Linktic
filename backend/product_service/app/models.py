from sqlalchemy import Column, Integer, String, Float, Boolean
from .db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(String(1024), nullable=True)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
