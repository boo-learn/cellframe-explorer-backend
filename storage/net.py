from shared.database import models

from sqlalchemy import select
from sqlalchemy.orm import Session


def get_all(session: Session, skip: int = 0, limit: int = 10) -> list[models.Net]:
    nets = session.scalars(select(models.Net).offset(skip).limit(limit))
    return list(nets.all())


def get_net_by_id(session: Session, id: int) -> models.Net | None:
    query = (
        select(models.Net).where(models.Net.id == id)
    )
    return session.execute(query).scalar_one_or_none()


def get_net_by_name(session: Session, name: str) -> models.Net | None:
    query = (
        select(models.Net).where(models.Net.name == name)
    )
    return session.execute(query).scalar_one_or_none()
