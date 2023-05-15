from typing import List, Optional
from pydantic import BaseModel


class Order(BaseModel):
    cost: int
    delivery_hours: List[str]
    regions: int
    weight: float

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class OrderCreate(BaseModel):
    orders: Optional[List[Order]] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class ResponseOrder(BaseModel):
    orders: Optional[List[Order]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


class ConfirmOrder(BaseModel):
    complete_time: Optional[str] = None
    courier_id: Optional[int] = None
    order_id: Optional[int] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class RequestConfirmOrder(BaseModel):
    complete_info: List[ConfirmOrder]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
