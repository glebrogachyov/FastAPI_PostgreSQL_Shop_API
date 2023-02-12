from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text
from database import Base


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    name = Column(String(50))
    price = Column(Float)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"Product | name: {self.name} price: {self.price} description: {self.description}"


class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    amount = Column(Integer)
