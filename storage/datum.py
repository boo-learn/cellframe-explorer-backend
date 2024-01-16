from sqlalchemy import select, func, desc, asc, cast
from sqlalchemy.orm import Session

from shared.database import models
from shared.types import DatumTypes

from .chain import get_chain


def get_datums_tx(
        session: Session, net_name: str,
        limit: int = 10, offset: int = 0, reverse: bool = False) -> list[models.Datum]:
    db_chain = get_chain(session, net_name, chain_name="main")
    # asc[↗] desc[↘]
    order = desc if reverse else asc
    query = (
        select(models.Datum)
        .where(
            (models.Datum.chain_id == db_chain.id) &
            (models.Datum.type == DatumTypes.DATUM_TX) &
            (models.Datum.sub_datum.op("->>")('ticker').isnot(None))
        )
        .order_by(order(models.Datum.created_at))
        .limit(limit)
        .offset(offset)
    )
    return list(session.scalars(query).all())


def get_datum_tx(
        session: Session, net_name: str, datum_hash: str) -> models.Datum | None:
    db_chain = get_chain(session, net_name, chain_name="main")
    query = select(models.Datum).where(
        (models.Datum.chain_id == db_chain.id) &
        (models.Datum.hash == datum_hash) &
        (models.Datum.type == DatumTypes.DATUM_TX) &
        (models.Datum.sub_datum.op("->>")('ticker').isnot(None))
    )
    return session.execute(query).scalar_one_or_none()


def count_datums_tx(session: Session, net_name: str) -> int:
    db_chain = get_chain(session, net_name, chain_name="main")
    query = (
        select(func.count())
        .select_from(models.Datum)
        .where(
            (models.Datum.chain_id == db_chain.id) &
            (models.Datum.type == DatumTypes.DATUM_TX) &
            (models.Datum.sub_datum.op("->>")('ticker').isnot(None))
        )
    )
    return session.execute(query).scalar()
