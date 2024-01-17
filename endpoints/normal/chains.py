from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

import schemas
import storage
from core import depends

router = APIRouter(prefix="/chains", tags=["CHAINS"])


@router.get("", response_model=list[schemas.Chain])
def get_chains(session: Session = Depends(depends.sync_db_session), skip: int = 0, limit: int = 10):
    chains = storage.chain.get_all(session, skip, limit)
    return chains
