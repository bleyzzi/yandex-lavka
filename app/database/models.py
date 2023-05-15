from sqlalchemy import Table, JSON, Identity, Float, DateTime
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from app.database.database import Base


courier = Table(
    "courier",
    Base.metadata,
    Column("courier_id", Integer, Identity(start=1, cycle=True), primary_key=True),
    Column("courier_type", String),
    Column("regions", JSON),
    Column("working_hours", JSON)
)


order = Table(
    "order",
    Base.metadata,
    Column("cost", Integer),
    Column("delivery_hours", JSON),
    Column("order_id", Integer, Identity(start=1, cycle=True), primary_key=True),
    Column("regions", Integer),
    Column("weight", Float),
    Column("completed_time", DateTime, default=None),
    Column("courier_delivers_id", Integer, default=None)
)