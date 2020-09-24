from app.api.routes import router as api_router
from app.core import config, tasks
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


async def not_implemented_exception_handler(*_):
    return JSONResponse(
        status_code=500,
        content={"message": "Feature not implemented (yet)"},
    )


def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.add_exception_handler(NotImplementedError, not_implemented_exception_handler)

    app.include_router(api_router, prefix=config.API_PREFIX)

    return app


app = get_application()
