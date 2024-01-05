from fastapi import FastAPI
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
