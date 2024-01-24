from typing import Callable
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import warnings
import sqlalchemy

from core.const import (
    OPEN_API_DESCRIPTION,
    OPEN_API_TITLE,
)
import endpoints
from endpoints.normal import (
    nets, chains, blocks
)
from core.version import __version__

app = FastAPI(
    title=OPEN_API_TITLE,
    description=OPEN_API_DESCRIPTION,
    version=__version__,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)


@app.middleware("http")
async def cors_middleware(request: Request, call_next: Callable):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


app.include_router(endpoints.router)
app.include_router(nets.router)
app.include_router(chains.router)
app.include_router(blocks.router)
