from app.router.couriers import router as router_courier
from app.router.orders import router as router_order

from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware


limiter = Limiter(key_func=get_remote_address, application_limits=["10/second"], key_style="endpoint")


def get_application() -> FastAPI:
    application = FastAPI(
        title="Yandex shop"
    )
    application.include_router(router_courier)
    application.include_router(router_courier)
    return application


app = get_application()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)