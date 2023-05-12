from src.app.router import router

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter


def get_application() -> FastAPI:
    application = FastAPI(
        title="Yandex shop"
    )
    FastAPILimiter.init(application)
    application.include_router(router)

    return application


app = get_application()
