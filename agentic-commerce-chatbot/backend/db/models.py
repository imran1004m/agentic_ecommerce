from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text, ForeignKey
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    category = Column(String)
    brand = Column(String)
    pack_size = Column(String)
    price = Column(Numeric)
    availability = Column(Boolean, default=True)
    embedding = Column(Vector(1536))


class Cart(Base):
    __tablename__ = "carts"

    session_id = Column(String, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer)


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    session_id = Column(String)
    status = Column(String)
    total = Column(Numeric)
