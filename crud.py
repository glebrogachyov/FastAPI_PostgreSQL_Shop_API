from sqlalchemy.orm import Session

import models
import schemas

"""
Нужны методы:
        1) Создать новый товар (минимальное описание обязательно - имя, цена, остальное опционально)
        2) Удалить существующий товар 
    3) Вывести все товары с фильтрацией и сортировкой (но это опционально, по дефолту выводить как есть)
        4) Добавить товар в корзину в нужном кол-ве (если кол-во 0, значит удалить)
    5) Получить всю корзину (минимальное описание товаров + кол-во, а также стоимость всей корзины)
    6) 
"""


def create_product(db: Session, product: schemas.DetailedProductIn):
    try:
        print(f"adding new product: {product}")
        db_product = models.Product(name=product.name, price=product.price, description=product.description)
        print(f"product db repr: {db_product}")
        db.add(db_product)
        db.commit()
    except Exception as e:
        return {"message": f"error. {e}"}
    return {"message": f"created product: {db_product.name} price: {db_product.price}"}


def remove_product(db: Session, product_id: int):
    try:
        db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if db_product:
            db.delete(db_product)
            db.commit()
        else:
            return {"message": f"no item with id {product_id}"}
    except Exception as e:
        return {"message": "database error. " + repr(e)}
    return {"message": f"removed {db_product.name} {db_product.price}"}


def list_products(db: Session,
                  names_filter_list=None,
                  min_price=None,
                  max_price=None,
                  name_order_by=None,
                  price_order_by=None):
    try:
        # Добавить фильтрацию
        db_products = db.query(models.Product).filter(models.Product.id > 0).all()
        print(db_products)
    except Exception as e:
        return {"message": "database error. " + repr(e)}
    return db_products


def get_product_description(db: Session, product_id):
    try:
        db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not db_product:
            return {"message": f"no item with id {product_id}"}
    except Exception as e:
        return {"message": "database error. " + repr(e)}
    return db_product


def add_to_cart(db: Session, product):
    try:
        is_product_exist = db.query(models.Product).filter(models.Product.id == product.id).first()
        if not is_product_exist:
            return {"message": f"product with id {product.id} doesn't exist"}
        # Дописать проверку на наличие товара в тележке: если нет, тогда добавить, если не ноль, иначе - изменить кол-во

        is_product_in_cart = db.query(models.Cart).filter(models.Cart.product_id == product.id).first()
        if not is_product_in_cart:
            if product.amount == 0:
                print(db, product.id)
                return {"message": f"no such product with id {product.id} in cart. nothing to remove."}
            cart_product = models.Cart(product_id=product.id, amount=product.amount)
            db.add(cart_product)
        else:
            if product.amount == 0:
                db.delete(is_product_in_cart)
            else:
                is_product_in_cart.amount = product.amount
        db.commit()
    except Exception as e:
        return {"message": f"error adding product with id {product.id} to cart. {repr(e)}"}
    return {"message": f"done. {product.id=} amount set to {product.amount=}"}


def list_cart(db: Session):
    try:
        t_c, t_p = models.Cart, models.Product
        query = db.query(t_p.id, t_p.name, t_p.price, t_c.amount).select_from(t_c).join(t_p, t_c.product_id == t_p.id)
        cart_items = query.all()
        keys_ = schemas.ProductInCart.__fields__.keys()
        for idx, item in enumerate(cart_items):
            cart_items[idx] = schemas.ProductInCart(**{k: v for k, v in zip(keys_, item)})
    except Exception as e:
        return {"message": "database error. " + repr(e)}
    return cart_items
