from datetime import date
from pydantic import BaseModel


class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: date
    status: bool = False


class OrderIn(BaseModel):
    user_id: int
    product_id: int
    order_date: date
    status: bool = False
