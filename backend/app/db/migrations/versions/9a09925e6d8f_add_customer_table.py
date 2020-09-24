"""Add customer table

Revision ID: 9a09925e6d8f
Revises: 3f592d7f0c9d
Create Date: 2020-09-24 17:09:27.510371

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic
revision = "9a09925e6d8f"
down_revision = "3f592d7f0c9d"
branch_labels = None
depends_on = None


def create_customer_table() -> None:
    op.create_table(
        "customers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.Text, nullable=False),
        sa.Column("last_name", sa.Text, nullable=False),
        sa.Column("email", sa.Text, nullable=False, unique=False),  # TODO: make unique
        sa.Column("phone", sa.Text, nullable=False),
        sa.Column("street", sa.Text, nullable=False),
        sa.Column("city", sa.Text, nullable=False),
        sa.Column("state", sa.Text, nullable=False),
        sa.Column("zip", sa.Text, nullable=False),
        sa.Column("country", sa.Text, nullable=False),
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
        CREATE TRIGGER tr_customers_update_timestamp
        BEFORE UPDATE ON customers
        FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at();
        """
    )


def upgrade() -> None:
    create_customer_table()


def downgrade() -> None:
    op.drop_table("customers")
