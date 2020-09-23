import logging
import os
import pathlib
import sys
from logging.config import fileConfig

import alembic
from sqlalchemy import create_engine, engine_from_config, pool

from psycopg2 import DatabaseError

# we're appending the app directory to our path here so that we can import config easily
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.core.config import (
    DATABASE_URL,
    POSTGRES_DB,
)  # IT MUST BE ABOVE THE sys.path.append(...) call


# Alembic Config object, which provides access to values within the .ini file
config = alembic.context.config

# Interpret the config file for logging
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode
    """

    db_suffix = os.environ.get("DB_SUFFIX", "")
    db_url = f"{DATABASE_URL}{db_suffix}"

    # handle testing config for migrations
    if "test" in db_suffix:
        # connect to primary db
        default_engine = create_engine(str(DATABASE_URL), isolation_level="AUTOCOMMIT")
        # drop testing db if it exists and create a fresh one
        with default_engine.connect() as default_conn:
            default_conn.execute(f"DROP DATABASE IF EXISTS {POSTGRES_DB}{db_suffix}")
            default_conn.execute(f"CREATE DATABASE {POSTGRES_DB}{db_suffix}")

    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", db_url)

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        alembic.context.configure(connection=connection, target_metadata=None)

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """

    db_suffix = os.environ.get("DB_SUFFIX", "")

    if "test" in db_suffix:
        raise DatabaseError(
            "Running testing migrations offline currently not permitted."
        )

    alembic.context.configure(url=str(DATABASE_URL))

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
