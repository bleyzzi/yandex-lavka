from pydantic import BaseModel


class CourierCreate(BaseModel):
    id: int
    Courier_type: int
    Regions: str
    Working_hours: str


class CourierTypeCreate(BaseModel):
    id: int
    type: str


class Courier(BaseModel):
    id: int
    Courier_type: int
    Regions: str
    Working_hours: str

    class Config:
        orm_mode = True