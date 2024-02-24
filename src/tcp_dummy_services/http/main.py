from tcp_dummy_services.core import logger
from tcp_dummy_services.core import settings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tcp_dummy_services.api.v1.things.router import api_router as things_v1_router
from tcp_dummy_services.api.v1.stuff.router import api_router as stuff_v1_router


def include_routers(app: FastAPI):
    """Include routers for every application

    Args:
        app (_type_): _description_
    """
    logger.debug("Including routers")
    if settings.THINGS_ENABLED:
        app.include_router(things_v1_router)

    # Only include if settings.STUFF_ENABLED is True
    if settings.STUFF_ENABLED and settings.THINGS_BASE_URL:
        app.include_router(stuff_v1_router)


def include_cors(app: FastAPI):
    """
    Include CORS configuration
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.CORS_ALLOWED_METHODS,
        allow_headers=settings.CORS_ALLOWED_HEADERS,
    )

    logger.debug("CORS initialized")


def start_application(app: FastAPI):
    """
    Start the application launching all required modules
    """

    include_cors(app)
    include_routers(app)

    return app


app: FastAPI = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    root_path=settings.ROOT_PATH,
)
start_application(app)
