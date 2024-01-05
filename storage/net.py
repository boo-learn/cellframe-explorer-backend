from shared.database import models

from sqlalchemy import select
from sqlalchemy.orm import Session


def get_net_by_id(session: Session, id: int) -> models.Net | None:
    return session.scalar(select(models.Net).where(models.Net.id == id))


def get_net_by_name(session: Session, name: str) -> models.Net | None:
    return session.scalar(select(models.Net).where(models.Net.name == name))