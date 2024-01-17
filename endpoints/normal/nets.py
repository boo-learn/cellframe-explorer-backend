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

router = APIRouter(prefix="/nets", tags=["NETS"])


@router.get("", response_model=list[schemas.Net])
def get_nets(session: Session = Depends(depends.sync_db_session), skip: int = 0,
             limit: int = 10):
    nets = storage.net.get_all(session, skip, limit)
    return nets


@router.get("/by_name/{name}", response_model=schemas.Net)
def get_net_by_name(name: str, session: Session = Depends(depends.sync_db_session)):
    net = storage.net.get_net_by_name(session, name)
    if net is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Net with name={name} does not exist",
        )

    return net


@router.get("/{net_id}", response_model=schemas.Net)
def get_net_by_id(net_id: int, session: Session = Depends(depends.sync_db_session)):
    net = storage.net.get_net_by_id(session, net_id)
    if net is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Net with id={net_id} does not exist",
        )

    return net
