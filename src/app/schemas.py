from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class CourierCreate(BaseModel):
    Name: str
    Courier_type: int
    Regions: List[int]
    Working_hours: List[str]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

        schema_extra = {
            "example": {
                "Name": "Ivan Ivanov",
                "Courier_type": 1,
                "Regions": [1, 2, 3],
                "Working_hours": ["13:00-14:00"],
            }
        }


class Courier(BaseModel):
    id: int
    Name: str
    Courier_type: str
    Regions: List[int]
    Working_hours: List[str]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class OrderCreate(BaseModel):
    Weight: float
    Region: int
    Delivery_time: str
    Cost: float

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

        schema_extra = {
            "example": {
                "Weight": 1000.01,
                "Region": 1,
                "Delivery_time": "13:00-14:00",
                "Cost": 1200.01
            }
        }


class Order(BaseModel):
    id: int
    Weight: float
    Region: int
    Delivery_time: str
    Cost: float

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class ResponseCourier(BaseModel):
    status: str
    data: Optional[List[Courier]] = None
    details: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class ResponseOrder(BaseModel):
    status: str
    data: Optional[List[Order]] = None
    details: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class RequestConfirmOrderCreate(BaseModel):
    Courier_id: int
    Order_id: int
    Time: str
    Status: str

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

        schema_extra = {
            "example": {
                "Courier_id": 1,
                "Order_id": 1,
                "Time": "13:00",
                "Status": "success"
            }
        }


class RequestRatingSalary(BaseModel):
    start_date: datetime
    end_date: datetime


class ResponseConfirmOrder(BaseModel):
    status: str
    data: Optional[List[RequestConfirmOrderCreate]] = None
    details: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class RatingSalary(BaseModel):
    rating: Optional[float] = None
    salary: Optional[float] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class ResponseRatingSalary(BaseModel):
    status: str
    data: Optional[RatingSalary] = None
    details: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


