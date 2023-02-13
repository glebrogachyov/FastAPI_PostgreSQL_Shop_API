import uvicorn
from fastapi import FastAPI, Query, Depends, Response
from fastapi.responses import RedirectResponse

from typing import Literal

from test_data import test_items
from schemas import *
from database import SessionLocal, engine
import crud
import models


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> RedirectResponse:
    """ Перенаправление на страницу документации OpenAPI """
    return RedirectResponse(url="http://localhost:8000/docs")


@app.post("/init_tables")
def init_tables(response: Response,
                create_empty: bool = Query(default=False, description="Создать без записей"),
                db=Depends(get_db)):
    """ Создать и наполнить таблицы тестовыми данными """
    result = crud.init_tables()
    if not create_empty:
        for item in test_items:
            crud.create_product(db, DetailedProductIn(**item))
    response.status_code = result["status_code"]
    return result["response"]


@app.delete("/drop_tables")
def drop_tables(response: Response):
    """ Удалить таблицы и данные """
    result = crud.drop_tables()
    response.status_code = result["status_code"]
    return result["response"]


@app.get("/products", response_model=list[BaseProduct] | dict)
def search_products(response: Response,
                    names: set[str] | None = Query(default=None, max_length=50, title="Search keywords"),
                    min_price: float | None = Query(default=None, gt=0),
                    max_price: float | None = Query(default=None, gt=0),
                    name_order_by: Literal["asc", "desc"] | None = None,
                    price_order_by: Literal["asc", "desc"] | None = None,
                    db=Depends(get_db)):
    """ Получить список названий товаров, с возможностью фильтрации (поиска) и сортировки по названию и (или) цене """
    result = crud.list_products(db, names, min_price, max_price, name_order_by, price_order_by)
    response.status_code = result["status_code"]
    return result["response"]


@app.get("/products/{product_id}", response_model=DetailedProductIn | dict)
def get_product_description(response: Response, product_id: int, db=Depends(get_db)):
    """ Получить детальное описание товара по его идентификатору """
    result = crud.get_product_description(db, product_id)
    response.status_code = result["status_code"]
    return result["response"]


@app.get("/cart")
def list_cart(response: Response, db=Depends(get_db)):
    """ Получить всю корзину """
    result = crud.list_cart(db)
    response.status_code = result["status_code"]
    return result["response"]


@app.post("/products")
def create_product(response: Response, product: DetailedProductIn, db=Depends(get_db)):
    """ Создать новый товар """
    result = crud.create_product(db, product)
    response.status_code = result["status_code"]
    return result["response"]


@app.delete("/products/{product_id}")
def remove_product(response: Response, product_id: int, db=Depends(get_db)):
    """ Удалить существующий товар """
    result = crud.remove_product(db, product_id)
    response.status_code = result["status_code"]
    return result["response"]


@app.patch("/cart")
def add_to_cart(response: Response, product_to_cart: ProductToCart, db=Depends(get_db)):
    """ Добавить товар в корзину, поменять количество товара в корзине. Количество = 0 уберёт товар из корзины """
    result = crud.add_to_cart(db, product_to_cart)
    response.status_code = result["status_code"]
    return result["response"]


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-init", "--initialize")
    args = parser.parse_args()

    if args.initialize:
        models.Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        for item in test_items:
            crud.create_product(db, DetailedProductIn(**item))
        db.close()
    uvicorn.run(app, host="localhost", port=8000)
