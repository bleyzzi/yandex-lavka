from typing import List, Optional, Any

from fastapi import HTTPException
from pydantic import BaseModel, Field, validator
import re
from starlette import status


class CourierVal(BaseModel):
    courier_type: str = Field("AUTO",
                              description="Курьер может быть трех типов: AUTO, BIKE, FOOT")
    regions: List[int] = Field([1])
    working_hours: List[str] = Field(["12:00-14:00"],
                                     description="Строка должна быть вида 12:00-14:00")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

    @validator('courier_type')
    def type_match(cls, v):
        if v not in ['AUTO', 'BIKE', 'FOOT']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Тип курьера может быть только AUTO, BIKE, FOOT")
        return v

    @validator('regions')
    def regions_match(cls, v):
        for elem in v:
            if type(elem) != int:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Регион задается целым числом")
        return v

    @validator('working_hours')
    def list_match(cls, v):
        reg = r'[0-2][0-9]:[0-5][0-9]-[0-2][0-9]:[0-5][0-9]'
        for elem in v:
            if not bool(re.search(reg, elem)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Проверьте введенное время")
        return v


class Courier(BaseModel):
    courier_id: int
    courier_type: str
    regions: List[int]
    working_hours: List[str]


class CourierCreate(BaseModel):
    couriers: List[CourierVal]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class ResponseCourier(BaseModel):
    couriers: Optional[List[Courier]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


class ResponseCourierWithId(BaseModel):
    courier_id: Optional[int] = None
    courier_type: Optional[str] = None
    regions: Optional[List[int]] = None
    working_hours: Optional[List[str]] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class ResponseCourierCreate(BaseModel):
    couriers: List[ResponseCourierWithId]

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
