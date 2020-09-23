from sqlalchemy import Boolean, Column, Integer, Numeric, Table, Text

from .base import metadata, default_timestamps_auditing

products_table = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False, index=True),
    Column("description", Text),
    Column(
        "available",
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    ),
    Column("price", Numeric(10, 2), nullable=False),
    *default_timestamps_auditing
)
