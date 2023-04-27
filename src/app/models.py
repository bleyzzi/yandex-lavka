from typing import List, Dict
from fastapi import FastAPI
from datetime import time
from pydantic import BaseModel
from enum import Enum
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, JSON


metadata = MetaData()


courier_type = Table(
    "courier_type",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("type", String, nullable=False)
)


courier = Table(
    "courier",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("Courier_type", Integer, ForeignKey("courier_type.id")),
    Column("Regions", String),
    Column("Working_hours", String)
)