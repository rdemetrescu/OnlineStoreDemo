import os
import uuid
import warnings
from typing import Any, Iterator

import alembic
import alembic.config
import docker as pydocker
import pytest
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient


@pytest.fixture(scope="session")
def docker() -> pydocker.APIClient:
    # base url is the unix socket we use to communicate with docker
    return pydocker.APIClient(base_url="unix://var/run/docker.sock", version="auto")


@pytest.fixture(scope="session", autouse=True)
def postgres_container(docker: pydocker.APIClient) -> Any:
    """
    Use docker to spin up a postgres container for the duration of the testing session.

    Kill it as soon as all tests are run.

    DB actions persist across the entirety of the testing session.
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # pull image from docker
    image = "postgres:12.4-alpine"
    docker.pull(image)

    # create the new container using
    # the same image used by our database
    container = docker.create_container(
        image=image,
        name=f"test-postgres-{uuid.uuid4()}",
        detach=True,
    )

    docker.start(container=container["Id"])

    config = alembic.config.Config("alembic.ini")

    try:
        os.environ["DB_SUFFIX"] = "_test"
        alembic.command.upgrade(config, "head")
        yield container
        alembic.command.downgrade(config, "base")
    finally:
        # remove container
        # TODO: check the reason for the container been already killed at this point
        # docker.kill(container["Id"])
        docker.remove_container(container["Id"])


# Create a new application for testing
@pytest.fixture
def app() -> FastAPI:
    from app.api.server import get_application

    return get_application()


# Grab a reference to our database when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


# Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> Iterator[AsyncClient]:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client
