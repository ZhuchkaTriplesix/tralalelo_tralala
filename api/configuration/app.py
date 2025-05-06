from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from configuration.router import Router


class App:
    def __init__(self):
        self._app: FastAPI = FastAPI(
            title="TernHost API",
            description="TernHost api",
            docs_url=None,
            redoc_url=None,
            openapi_url="/api/openapi.json",
        )
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "DELETE", "PATCH"],
            allow_headers=["*"]
        )
        self._register_routers()

    def _register_routers(self) -> None:
        for router, prefix, tags in Router.routers:
            self._app.include_router(router=router, prefix=prefix, tags=tags)

    @property
    def app(self) -> FastAPI:
        return self._app

