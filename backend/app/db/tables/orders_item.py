from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Table

from .base import default_timestamps_auditing, metadata

order_items_table = Table(
    "order_items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("order_id", Integer, ForeignKey("orders.id"), nullable=False),
    Column("product_id", Integer, ForeignKey("product.id"), nullable=False),
    Column("product_name", String, nullable=False),
    Column("price", Numeric(10, 2), nullable=False),
    Column("qty", Integer, nullable=False),
    Column("total", Numeric(10, 2), nullable=False),
    *default_timestamps_auditing()
)
