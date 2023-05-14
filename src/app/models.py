from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, JSON, Identity, Float, DateTime
from sqlalchemy.sql.schema import Sequence

metadata = MetaData()


courier = Table(
    "courier",
    metadata,
    Column("courier_id", Integer, Identity(start=1, cycle=True), primary_key=True),
    Column("courier_type", String),
    Column("regions", JSON),
    Column("working_hours", JSON)
)

order = Table(
    "order",
    metadata,
    Column("cost", Integer),
    Column("delivery_hours", JSON),
    Column("order_id", Integer, Identity(start=1, cycle=True), primary_key=True),
    Column("regions", Integer),
    Column("weight", Float),
    Column("completed_time", DateTime, default=None),
)

