from sqlalchemy import select, func, desc, asc
from sqlalchemy.orm import Session

from shared.database import models
from .chain import get_chain
from ._common import get_atoms


def get_events(
        session: Session, net_name: str, chain_name: str,
        limit: int = 10, offset: int = 0, reverse: bool = False) -> list[models.Block]:
    return get_atoms("block", session, net_name, chain_name, limit, offset, reverse)


def get_event(session: Session, net_name:str, chain_name: str, event_hash: str) -> models.Event | None:
    db_chain = get_chain(session, net_name=net_name, chain_name=chain_name)
    query = (
        select(models.Event)
        .where(models.Event.id == f"{event_hash}{db_chain.id}")
    )
    return session.execute(query).scalar_one_or_none()
