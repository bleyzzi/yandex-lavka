from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum


class CourierType(Enum):
    foot = "foot"
    bicycle = "bicycle"
    auto = "auto"


class Courier(BaseModel):
    courier_id: int
    courier_type: CourierType
    regions: List[int]
    working_hours: List[str]

