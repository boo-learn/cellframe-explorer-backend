from typing import Literal
from sqlalchemy import select, func, desc, asc
from sqlalchemy.orm import Session

from shared.database import models
from .chain import get_chain


def get_atoms(
        subtype: Literal["block", "event"],
        session: Session, net_name: str, chain_name: str,
        limit: int = 10, offset: int = 0, reverse: bool = False
) -> list[models.Block | models.Event]:
    db_chain = get_chain(session, net_name, chain_name)
    # asc[↗] desc[↘]
    order = desc if reverse else asc
    # select model by subtype
    model = models.Block if subtype == "block" else models.Event
    print(f"{db_chain.id=}")
    print(f"{limit=}")
    print(f"{offset=}")
    print(f"{subtype=}")
    query = (
        select(model)
        .where(
            (model.chain_id == db_chain.id)
        )
        .order_by(order(model.created_at))
        .limit(limit)
        .offset(offset)
    )
    return list(session.scalars(query).all())
