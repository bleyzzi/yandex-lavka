from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, JSON, Identity, Float
from sqlalchemy.sql.schema import Sequence

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
    Column("id", Integer, Sequence("confirm_order_id_seq", metadata=metadata, start=1), primary_key=True),
    Column("Courier_id", Integer, ForeignKey("courier.id")),
    Column("Order_id", Integer, ForeignKey("order.id"), index=True, unique=True),
    Column("Time", String),
    Column("Status", String)
)
