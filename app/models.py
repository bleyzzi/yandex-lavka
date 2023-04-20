from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel

class Courier(BaseModel):
    courier_id: int
    courier_type: str
    regions: List[int]
    working_hours: List[str]
