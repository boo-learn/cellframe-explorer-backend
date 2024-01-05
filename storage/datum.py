from sqlalchemy import select, func, desc, cast
from sqlalchemy.orm import Session

from shared.database import models
from shared.types import DatumTypes

from .chain import get_chain


def get_datums_tx(
        session: Session, net_name: str,
        limit: int = 10, offset: int = 0, reverse: bool = False) -> list[models.Datum]:
    db_chain = get_chain(session, net_name, chain_name="main")
    query = (
        select(models.Datum)
        .where(
            (models.Datum.chain_id == db_chain.id) &
            (models.Datum.type == DatumTypes.DATUM_TX) &
            (models.Datum.sub_datum.op("->>")('ticker').isnot(None))
        )

        .limit(limit)
        .offset(offset)
    )
    if reverse:
        # datums_tx.reverse()
        query = query.order_by(models.Datum.created_at)
    else:
        query = query.order_by(desc(models.Datum.created_at))
    datums_tx = list(session.scalars(query).all())
    return datums_tx


def get_datum_tx(
        session: Session, net_name: str, datum_hash: str) -> models.Datum:
    db_chain = get_chain(session, net_name, chain_name="main")
    query = select(models.Datum).where(
        (models.Datum.chain_id == db_chain.id) &
        (models.Datum.hash == datum_hash) &
        (models.Datum.type == DatumTypes.DATUM_TX) &
        (models.Datum.sub_datum.op("->>")('ticker').isnot(None))
    )
    return session.scalar(query)


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
