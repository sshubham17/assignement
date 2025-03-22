from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as PgEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum

Base = declarative_base()

class StatusEnum(Enum):
    FAILED = 'FAILED'
    COMPLETED = 'COMPLETED'
    PROCESSED = 'PROCESSED'
    PENDING = 'PENDING'

# Product Table
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

# Order Table
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float, nullable=False, default=0.0)
    status = Column('status', PgEnum(StatusEnum, name='status_enum'), nullable=False)
    order_items = relationship("OrderItem", back_populates="order")

# OrderItem Table (Many-to-Many relationship between Order & Product)
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")