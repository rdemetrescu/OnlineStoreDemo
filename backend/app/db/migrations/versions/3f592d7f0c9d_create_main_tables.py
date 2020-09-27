"""create products table

Revision ID: 3f592d7f0c9d
Revises:
Create Date: 2020-09-23 14:28:44.764840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "3f592d7f0c9d"
down_revision = None
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )


def create_product_table() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False, index=True),
        sa.Column("description", sa.Text),
        sa.Column(
            "available",
            sa.Boolean,
            nullable=False,
            default=False,
            server_default="false",
        ),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
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
        CREATE TRIGGER tr_products_update_timestamp
        BEFORE UPDATE ON products
        FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_product_table()


def downgrade() -> None:
    op.drop_table("products")
    op.execute("DROP FUNCTION update_updated_at")
