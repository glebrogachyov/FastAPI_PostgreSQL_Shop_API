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


def create_product(db: Session, product: schemas.DetailedProduct):
    try:
        db.add(models.Product)
        db.commit()
        # db.refresh()
    except:
        return {"message": "error."}
    return {"message": "done."}


def remove_product(product_id):
    ...


def list_products(names_filter_list, min_price, max_price, name_order_by, price_order_by):
    ...


def get_product_description(product_id):
    ...


def add_to_cart(product_id, amount):
    ...


def list_cart():
    ...
