from sqlalchemy import Column, Integer, Table, String, Numeric, ForeignKey


from .base import metadata, default_timestamps_auditing

orders_table = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", Integer, ForeignKey("customers.id"), nullable=False),
    Column("customer_name", String, nullable=False),
    # billing columns
    Column("billing_street", String, nullable=False),
    Column("billing_city", String, nullable=False),
    Column("billing_state", String, nullable=False),
    Column("billing_zip", String, nullable=False),
    Column("billing_country", String, nullable=False),
    # shipping columns
    Column("shipping_street", String, nullable=False),
    Column("shipping_city", String, nullable=False),
    Column("shipping_state", String, nullable=False),
    Column("shipping_zip", String, nullable=False),
    Column("shipping_country", String, nullable=False),
    #
    Column("total", Numeric(15, 2), nullable=False, default=0, server_default="0"),
    *default_timestamps_auditing(),
)
