from typing import List, Dict
from fastapi import FastAPI
from datetime import time
from pydantic import BaseModel
from enum import Enum
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON

class PairHours(BaseModel):
    beginning_working_hours: time
    ending_working_hours: time


class CourierType(Enum):
    foot = "foot"
    bike = "bike"
    car = "car"


class Courier(BaseModel):
    courier_id: int
    courier_type: CourierType
    regions: List[int]
    working_hours: List[PairHours]


metadata = MetaData()


courier_type = Table(
    "courier_type",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("type", String, nullable=False)
)


courier = Table(
    "courier",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("Courier type", String, ForeignKey("courier_type.id")),
    Column("Regions", JSON),
    Column("Working hours", JSON)
)