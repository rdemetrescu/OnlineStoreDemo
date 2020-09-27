"""add orders and order_items tables

Revision ID: df72542f1ecd
Revises: 9a09925e6d8f
Create Date: 2020-09-26 20:55:35.111325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "df72542f1ecd"
down_revision = "9a09925e6d8f"
branch_labels = None
depends_on = None


def create_orders_table() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True),
        # TODO: sa.Column("customer_id", sa.Integer, sa.ForeignKey("customers.id"), nullable=False),
        # TODO: sa.Column("customer_name", sa.String, nullable=False),
        # billing columns
        sa.Column("billing_street", sa.String, nullable=False),
        sa.Column("billing_city", sa.String, nullable=False),
        sa.Column("billing_state", sa.String, nullable=False),
        sa.Column("billing_zip", sa.String, nullable=False),
        sa.Column("billing_country", sa.String, nullable=False),
        # shipping columns
        sa.Column("shipping_street", sa.String, nullable=False),
        sa.Column("shipping_city", sa.String, nullable=False),
        sa.Column("shipping_state", sa.String, nullable=False),
        sa.Column("shipping_zip", sa.String, nullable=False),
        sa.Column("shipping_country", sa.String, nullable=False),
        #
        sa.Column(
            "total", sa.Numeric(15, 2), nullable=False, default=0, server_default="0"
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.execute(
        """
        CREATE TRIGGER tr_orders_update_timestamp
        BEFORE UPDATE ON orders
        FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at();
        """
    )


def create_order_items_table() -> None:
    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id"), nullable=False),
        sa.Column(
            "product_id", sa.Integer, sa.ForeignKey("products.id"), nullable=False
        ),
        sa.Column("product_name", sa.String, nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("qty", sa.Integer, nullable=False),
        sa.Column("total", sa.Numeric(10, 2), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.execute(
        """
        CREATE TRIGGER tr_order_items_update_timestamp
        BEFORE UPDATE ON orders
        FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at();
        """
    )


def upgrade() -> None:
    create_orders_table()
    create_order_items_table()


def downgrade() -> None:
    op.drop_table("order_items")
    op.drop_table("orders")
