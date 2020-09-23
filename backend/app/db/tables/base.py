from sqlalchemy import TIMESTAMP, Column, MetaData, func

metadata = MetaData()


default_timestamps_auditing = (
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    ),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    ),
)
