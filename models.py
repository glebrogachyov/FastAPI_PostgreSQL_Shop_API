from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from database import Base


class Product(Base):          # pk: product_id, name, price, brand_id
    __tablename__ = "product"
    id = Column(Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    name = Column(String(50))
    price = Column(Float)
    description = Column(Text, nullable=True)
    # items = relationship("Product", back_populates="items")

    # def __repr__(self):
    #     ...


class Cart(Base):             # product_id, amount
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    amount = Column(Integer)
    # items = relationship("Product")
