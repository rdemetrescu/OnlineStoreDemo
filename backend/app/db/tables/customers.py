from sqlalchemy import Column, Integer, String, Table

from .base import default_timestamps_auditing, metadata

customers_table = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False, unique=True),
    Column("phone", String, nullable=False),
    Column("street", String, nullable=False),
    Column("city", String, nullable=False),
    Column("state", String, nullable=False),
    Column("zip", String, nullable=False),
    Column("country", String, nullable=False),
    *default_timestamps_auditing()
)
