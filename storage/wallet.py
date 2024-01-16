from shared.database import models

from sqlalchemy import select
from sqlalchemy.orm import Session


def get_wallet_by_address(session: Session, address: str) -> models.Wallet | None:
    query = (
        select(models.Wallet, models.Net)
        .join(models.Net)
        .where(models.Wallet.addr == address)
    )
    return session.execute(query).scalar_one_or_none()
