from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import warnings
import sqlalchemy

from core.const import (
    OPEN_API_DESCRIPTION,
    OPEN_API_TITLE,
)
import endpoints
from core.version import __version__

# FIXME: fix warnings
warnings.filterwarnings("ignore", category=sqlalchemy.exc.SAWarning)

app = FastAPI(
    title=OPEN_API_TITLE,
    description=OPEN_API_DESCRIPTION,
    version=__version__,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.include_router(endpoints.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)