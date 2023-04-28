from datetime import datetime
from typing import List

from pydantic import BaseModel


class CourierCreate(BaseModel):
    Courier_type: int
    Regions: List[int]
    Working_hours: List[str]


class CourierTypeCreate(BaseModel):
    id: int
    type: str


class Courier(BaseModel):
    id: int
    Courier_type: str
    Regions: List[int]
    Working_hours: List[str]

    class Config:
        orm_mode = True