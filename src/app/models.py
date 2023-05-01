from typing import List, Dict
from fastapi import FastAPI
from datetime import time
from pydantic import BaseModel
from enum import Enum
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, JSON, Identity, Float

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
    Column("Name", String, nullable=False),
    Column("Courier_type", Integer, ForeignKey("courier_type.id")),
    Column("Regions", JSON),
    Column("Working_hours", JSON)
)


order = Table(
    "order",
    metadata,
    Column("id", Integer, Identity(start=1, cycle=True), primary_key=True),
    Column("Weight", Float),
    Column("Region", Integer),
    Column("Delivery_time", String),
    Column("Cost", Float)
)


confirm_order = Table(
    "confirm_order",
    metadata,
    Column("id", Integer, Identity(start=1, cycle=True), primary_key=True),
    Column("Courier_id", Integer, ForeignKey("courier.id")),
    Column("Order_id", Integer, ForeignKey("order.id")),
    Column("Status", String)
)
