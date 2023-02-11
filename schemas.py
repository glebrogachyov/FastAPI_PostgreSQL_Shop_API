from pydantic import BaseModel, constr, confloat, conint


class BaseProduct(BaseModel):
    name: constr(strip_whitespace=True, to_lower=True, max_length=50)
    price: confloat(ge=0)


class DetailedProduct(BaseProduct):
    description: constr(strip_whitespace=True) | None = None

    class Config:
        orm_mode = True


class ProductToCart(BaseModel):
    id: conint(ge=0)
    amount: conint(ge=0)

    class Config:
        orm_mode = True


class ProductInCart(BaseProduct):
    amount: conint(gt=0)
    total_price: confloat(ge=0)

    class Config:
        orm_mode = True


class Cart(BaseModel):
    items: list[ProductInCart]
    total_cost: conint(ge=0)

    class Config:
        orm_mode = True

