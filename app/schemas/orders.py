from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field, validator
from starlette import status
import re


class Order(BaseModel):
    cost: int = Field(1000,
                      description="Цена представлена целым числом")
    delivery_hours: List[str] = Field(["12:00-14:00"],
                                      description="Строка должна быть вида 12:00-14:00")
    regions: int = Field(1)
    weight: float = Field(1000.00)

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

    @validator('delivery_hours')
    def list_match(cls, v):
        reg = r'[0-2][0-9]:[0-5][0-9]-[0-2][0-9]:[0-5][0-9]'
        for elem in v:
            if not bool(re.search(reg, elem)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Проверьте введенное время")
        return v

    @validator('cost')
    def cost_match(cls, v):
        if type(v) != int:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Цена должна быть целым число")
        return v

    @validator('weight')
    def weight_match(cls, v):
        if type(v) != float:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Вес должен быть числом")

    @validator('regions')
    def regions_match(cls, v):
        if type(v) != int or not v >= 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Регион должен быть целым числом")


class OrderCreate(BaseModel):
    orders: List[Order]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class ResponseOrder(BaseModel):
    orders: Optional[List[Order]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


class ConfirmOrder(BaseModel):
    complete_time: str = Field("12:00",
                               description="Строка должна быть вида HH:MM")
    courier_id: int = Field(1)
    order_id: int = Field(1)

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

    @validator('complete_time')
    def list_match(cls, v):
        reg = r'[0-2][0-9]:[0-5][0-9]'
        if not bool(re.search(reg, v)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Проверьте введенное время")

        return v


class RequestConfirmOrder(BaseModel):
    complete_info: List[ConfirmOrder]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
