import datetime
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class Courier(BaseModel):
    courier_type: str
    regions: List[int]
    working_hours: List[str]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class CourierCreate(BaseModel):
    couriers: List[Courier]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class ResponseCourier(BaseModel):
    couriers: Optional[List[Courier]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


class ResponseCourierWithId(BaseModel):
    courier_id: int
    courier_type: str
    regions: List[int]
    working_hours: List[str]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class ResponseCourierCreate(BaseModel):
    couriers: List[ResponseCourierWithId]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


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
    complete_time: Optional[datetime] = None
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


class RequestMetaInfo(BaseModel):
    courier_id: Optional[int] = None
    courier_type: Optional[str] = None
    regions: Optional[List[int]] = None
    working_hours: Optional[List[str]] = None
    rating: Optional[int] = None
    earnings: Optional[int] = None
