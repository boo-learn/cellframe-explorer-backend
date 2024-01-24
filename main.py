from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
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
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        status_code=500, content=jsonable_encoder({"code": 500, "msg": "Internal Server Error"}))


app.include_router(endpoints.router)
app.include_router(nets.router)
app.include_router(chains.router)
app.include_router(blocks.router)
