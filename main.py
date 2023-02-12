import uvicorn
from fastapi import FastAPI, Query, Depends
from fastapi.responses import RedirectResponse

from typing import Literal

import models
from schemas import *
from database import SessionLocal, engine
import crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


"""
Добавить нормальные респонсы!!!!
"""


# db dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="http://localhost:8000/docs")


@app.get("/products", response_model=list[DetailedProduct], response_model_include={"id", "name", "price"})
def search_products(names: set[str] | None = Query(default=None, max_length=50, title="Search keywords"),
                    min_price: float | None = Query(default=None, gt=0),
                    max_price: float | None = Query(default=None, gt=0),
                    order_by_name: Literal["asc", "desc"] | None = None,
                    order_by_price: Literal["asc", "desc"] | None = None,
                    db=Depends(get_db)):  # -> list[Product] | None:
    """ Получить список названий товаров, с возможностью фильтрации (поиска) и сортировки по названию и (или) цене """
    result = crud.list_products(db)
    return result


@app.get("/products/{product_id}", response_model=DetailedProduct | dict, response_model_exclude={"id"})
def product_description(product_id: int, db=Depends(get_db)):
    """ Получить детальное описание товара по его идентификатору """
    result = crud.get_product_description(db, product_id)
    # print(result)
    return result


@app.get("/cart")
def list_cart(db=Depends(get_db)):
    """ Получить всю корзину """
    result = Cart(items=crud.list_cart(db))
    print(f"{result=}")
    return result


@app.post("/new_product")
def create_product(product: DetailedProductIn, db=Depends(get_db)):
    """ Создать новый товар """
    result = crud.create_product(db, product)
    print(result)
    return result


@app.delete("/{product_id}")
def remove_product(product_id: int, db=Depends(get_db)):
    """ Удалить существующий товар """
    result = crud.remove_product(db, product_id)
    print(result)
    return result


@app.patch("/product_to_cart/")
def add_to_cart(product_to_cart: ProductToCart, db=Depends(get_db)):
    """ Добавить товар в корзину, поменять количество товара в корзине """
    result = crud.add_to_cart(db, product_to_cart)
    return result


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
