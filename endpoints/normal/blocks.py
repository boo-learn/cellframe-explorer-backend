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

router = APIRouter(prefix="/blocks", tags=["BLOCKS"])


@router.get("", response_model=list[schemas.Block])
def get_blocks(
        net_name: str, chain_name: str,
        skip: int = 0, limit: int = 10, reverse: bool = False,
        session: Session = Depends(depends.sync_db_session)):
    blocks = storage.block.get_blocks(session, net_name, chain_name, limit=limit, offset=skip, reverse=reverse)
    print(f"{len(blocks)=}")
    return blocks
