from sqlalchemy import select, func
from sqlalchemy.orm import Session, lazyload, subqueryload, selectinload

from shared.database import models
from logger import logIt


def get_all(session: Session, skip: int, limit: int) -> list[models.Chain]:
    chains = session.scalars(select(models.Chain).offset(skip).limit(limit))
    return list(chains.all())


def get_chain(session: Session, net_name: str, chain_name: str) -> models.Chain | None:
    return (
        session.execute(
            select(models.Chain)
            .join(models.Chain.net)
            .where(
                (models.Chain.name == chain_name) & (models.Net.name == net_name)
            )
            # .join(models.Atom)
        )
    ).scalar_one_or_none()
