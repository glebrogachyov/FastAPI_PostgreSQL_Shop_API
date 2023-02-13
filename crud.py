from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

import models
import schemas
from database import engine


def filtrate(query, names=None, min_price=None, max_price=None, name_order_by=None, price_order_by=None):
    if names:
        query = query.filter(or_(*[models.Product.name.like(f"%{name_.lower()}%") for name_ in names]))

    if min_price:
        query = query.filter(models.Product.price >= min_price)
    if max_price:
        query = query.filter(models.Product.price <= max_price)

    if name_order_by == "asc":
        query = query.order_by(models.Product.name)
    elif name_order_by == "desc":
        query = query.order_by(desc(models.Product.name))

    if price_order_by == "asc":
        query = query.order_by(models.Product.price)
    elif price_order_by == "desc":
        query = query.order_by(desc(models.Product.price))

    return query


def create_product(db: Session, product: schemas.DetailedProductIn):
    try:
        db_product = models.Product(name=product.name, price=product.price, description=product.description)
        db.add(db_product)
        db.commit()
    except Exception as e:
        return {"status_code": 500, "response": {"message": f"error. debug: {e}"}}
    return {"status_code": 201,
            "response": {"message": f"created product: {db_product.name} | price: {db_product.price}"}}


def remove_product(db: Session, product_id: int):
    try:
        db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if db_product:
            db.delete(db_product)
            db.commit()
        else:
            return {"status_code": 404, "response": {"message": f"no item with id {product_id}"}}
    except Exception as e:
        return {"status_code": 500, "response": {"message": "database error. debug: " + repr(e)}}
    return {"status_code": 200, "response": {"message": f"removed {db_product.name}; price: {db_product.price}"}}


def list_products(db: Session, names=None, min_price=None, max_price=None, name_order_by=None, price_order_by=None):
    try:
        query = filtrate(db.query(models.Product), names=names, min_price=min_price, max_price=max_price,
                         name_order_by=name_order_by, price_order_by=price_order_by)
        db_products = query.all()

    except Exception as e:
        return {"status_code": 500, "response": {"message": "database error. debug: " + repr(e)}}
    return {"status_code": 200, "response": db_products}


def get_product_description(db: Session, product_id):
    try:
        db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not db_product:
            return {"status_code": 404, "response": {"message": f"no item with id {product_id}"}}
    except Exception as e:
        return {"status_code": 500, "response": {"message": "database error. debug: " + repr(e)}}
    return {"status_code": 200, "response": db_product}


def add_to_cart(db: Session, product):
    try:
        is_product_exist = db.query(models.Product).filter(models.Product.id == product.id).first()
        if not is_product_exist:
            return {"status_code": 404, "response": {"message": f"product with id {product.id} doesn't exist"}}

        product_in_cart = db.query(models.Cart).filter(models.Cart.product_id == product.id).first()
        if not product_in_cart:
            if product.amount == 0:
                return {"status_code": 404, "response": {"message": f"no product with id {product.id} in cart."}}
            cart_product = models.Cart(product_id=product.id, amount=product.amount)
            db.add(cart_product)
        else:
            if product.amount == 0:
                db.delete(product_in_cart)
            else:
                product_in_cart.amount = product.amount
        db.commit()
    except Exception as e:
        return {"status_code": 500,
                "response": {"message": f"error adding product with id {product.id} to cart. debug: {repr(e)}"}}
    return {"status_code": 200,
            "response": {"message": f"done. product with id {product.id} amount set to {product.amount}"}}


def list_cart(db: Session):
    try:
        crt, prd = models.Cart, models.Product
        query = db.query(prd.id, prd.name, prd.price, crt.amount).select_from(crt).join(prd, crt.product_id == prd.id)
        cart_items = query.all()
        keys_ = schemas.ProductInCart.__fields__.keys()
        for idx, item in enumerate(cart_items):
            cart_items[idx] = schemas.ProductInCart(**{k: v for k, v in zip(keys_, item)})
    except Exception as e:
        return {"status_code": 500, "response": {"message": "database error. debug: " + repr(e)}}
    return {"status_code": 200, "response": schemas.Cart(items=cart_items)}


def init_tables():
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        return {"status_code": 500, "response": {"message": "database error. debug: " + repr(e)}}
    return {"status_code": 200, "response": {"message": "tables created"}}


def drop_tables():
    try:
        models.Base.metadata.drop_all(bind=engine)
    except Exception as e:
        return {"status_code": 500, "response": {"message": "database error. debug: " + repr(e)}}
    return {"status_code": 200, "response": {"message": "tables dropped"}}
