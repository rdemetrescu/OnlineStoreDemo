from sqlalchemy import Boolean, Column, Integer, Numeric, Table, Text

from .base import metadata, default_timestamps_auditing

customers_table = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", Text, nullable=False),
    Column("last_name", Text, nullable=False),
    Column("email", Text, nullable=False, unique=True),
    Column("phone", Text, nullable=False),
    Column("street", Text, nullable=False),
    Column("city", Text, nullable=False),
    Column("state", Text, nullable=False),
    Column("zip", Text, nullable=False),
    Column("country", Text, nullable=False),
    *default_timestamps_auditing()
)
