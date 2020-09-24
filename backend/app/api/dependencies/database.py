from databases import Database
from starlette.requests import Request


def get_database(request: Request) -> Database:
    return request.app.state._db
