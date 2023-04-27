from src.app.router import router

from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI(
        title="Yandex shop"
    )
    application.include_router(router)

    return application


app = get_application()
