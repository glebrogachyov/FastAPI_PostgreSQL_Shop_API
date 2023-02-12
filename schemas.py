from pydantic import BaseModel, constr, confloat, conint, root_validator


class BaseProduct(BaseModel):
    id: conint(ge=0)
    name: constr(strip_whitespace=True, to_lower=True, max_length=50)
    price: confloat(ge=0)


class DetailedProduct(BaseProduct):
    description: constr(strip_whitespace=True) | None = None

    class Config:
        orm_mode = True


class DetailedProductIn(BaseModel):
    name: constr(strip_whitespace=True, to_lower=True, max_length=50)
    price: confloat(ge=0)
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
    total_price: confloat(ge=0) | None

    @root_validator
    def compute_total_price(cls, values) -> dict:
        values["total_price"] = values["price"] * values["amount"]
        return values

    class Config:
        orm_mode = True


class Cart(BaseModel):
    items: list[ProductInCart]
    cart_cost: confloat(ge=0) | None

    @root_validator
    def compute_cart_cost(cls, values) -> dict:
        cart_cost = 0
        for item in values["items"]:
            cart_cost += item.total_price
        values["cart_cost"] = cart_cost
        return values

    class Config:
        orm_mode = True

