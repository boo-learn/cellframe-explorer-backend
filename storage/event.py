from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session

from shared.database import models
from .chain import get_chain


def get_events(
        session: Session, net_name: str, chain_name: str,
        limit: int = 10, offset: int = 0, reverse: bool = False) -> list[models.Event]:
    # db_chain = session.scalar(select(models.Chain).where(models.Chain.name == chain_name))
    db_chain = get_chain(session, net_name=net_name, chain_name=chain_name)
    query = (
        select(models.Event)
        .where(
            (models.Event.chain_id == db_chain.id)
        )
        .limit(limit)
        .offset(offset)
    )
    events = list(session.scalars(query).all())
    if reverse:
        events.reverse()
        # atoms = query.order_by(desc(models.Atom.created_at))
    return events


def get_event(session: Session, net_name:str, chain_name: str, event_hash: str) -> models.Event | None:
    db_chain = get_chain(session, net_name=net_name, chain_name=chain_name)
    query = (
        select(models.Event)
        .where(models.Event.id == f"{event_hash}{db_chain.id}")
    )
    # print(f"id={db_chain.id}{event_hash}")
    return session.execute(query).scalar()
