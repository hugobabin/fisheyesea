"""fisheyesea main.py."""

import os
from collections.abc import Callable
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from rich.console import Console

from routers.countries import router as router_countries
from routers.fishingefforts import router as router_fishing_efforts
from services.etl import ServiceETL
from services.log import ServiceLog

console = Console()

routers = [router_fishing_efforts, router_countries]


async def init_routers(app: FastAPI) -> None:
    """Set up routers listed in {routers}."""
    for router in routers:
        app.include_router(router)
        console.print(f"✅ [bold green]set up router towards {router.prefix}")


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ANN201
    """Set up lifespan."""
    if os.getenv("WITH_ETL") == "true":
        console.print("[bold yellow]running etl scripts...")
        ServiceETL.process()
    await init_routers(app=app)
    console.print("✅ [bold cyan]fisheyesea is ready at http://127.0.0.1:8000")
    yield
    console.print("🌊​ [bold red]shutting down fisheyesea...")


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next: Callable) -> Any:  # noqa: ANN401
    """Handle HTTP logs."""
    response = await call_next(request)
    ServiceLog.info(
        f"{request.method} request on {request.url.path} - status is {response.status_code}",  # noqa: E501
    )
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle Exception logs."""
    ServiceLog.error(f"Exception on {request.method} {request.url}: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@app.get("/")
def get_root() -> dict:
    """Get root."""
    return {"Hello": "World"}
