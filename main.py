import uvicorn
from fastapi import FastAPI, Query, Depends
from fastapi.responses import RedirectResponse

from typing import Literal

import models
from schemas import *
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# db dependecy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="http://localhost:8000/docs")


@app.get("/products")   # , response_model_include={"name", "price"}) see: /tutorial/response-model/
def search_products(names: set[str] | None = Query(default=None, max_length=50, title="Search keywords"),
                    min_price: float | None = Query(default=None, gt=0),
                    max_price: float | None = Query(default=None, gt=0),
                    order_by_name: Literal["asc", "desc"] | False = False,
                    order_by_price: Literal["asc", "desc"] | False = False,
                    db=Depends(get_db)):  # -> list[Product] | None:
    """ Получить список названий товаров, с возможностью фильтрации (поиска) и сортировки по названию и (или) цене """
    # вызов метода БД
    if names:
        for name in names:
            print(name)
    return {"names": names, "min_price": min_price, "max_price": max_price,
            "order_by_name": order_by_name, "order_by_price": order_by_price}


@app.get("/products/{product_id}")
def product_description(product_id: int, db=Depends(get_db)):
    """ Получить детальное описание товара по его идентификатору """
    # Запрос полного описания товара в БД (с джойном таблицы подробной инфы)
    return {"product_id": product_id}


@app.post("/new_product")
def create_product(product: DetailedProduct, db=Depends(get_db)):
    """ Создать новый товар """
    return {"name": product.name, "price": product.price}


@app.patch("/product_to_cart/")
def add_to_cart(product_to_cart: ProductToCart, db=Depends(get_db)):
    """ Добавить товар в корзину, поменять количество товара в корзине """
    return {"ProductToCart": product_to_cart}


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
