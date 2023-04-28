from typing import List, Dict
from fastapi import FastAPI
from datetime import time
from pydantic import BaseModel
from enum import Enum
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, JSON, Identity


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
    Column("id", Integer, Identity(start=1, cycle=True), primary_key=True),
    Column("Courier_type", Integer, ForeignKey("courier_type.id")),
    Column("Regions", JSON),
    Column("Working_hours", JSON)
)