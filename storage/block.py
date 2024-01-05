from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session

from shared.database import models
from .chain import get_chain


def get_blocks(
        session: Session, net_name: str, chain_name: str,
        limit: int = 10, offset: int = 0, reverse: bool = False) -> list[models.Block]:
    db_chain = get_chain(session, net_name, chain_name)
    query = (
        select(models.Block)
        .where(
            (models.Block.chain_id == db_chain.id)
        )
        .order_by(desc(models.Block.created_at))
        .limit(limit)
        .offset(offset)
    )
    blocks = list(session.scalars(query).all())
    if reverse:
        blocks.reverse()
        # atoms = query.order_by(desc(models.Atom.created_at))
    return blocks


def get_block(session: Session, net_name: str, chain_name: str, block_hash: str) -> models.Event | None:
    db_chain = get_chain(session, net_name=net_name, chain_name=chain_name)
    query = (
        select(models.Block)
        .where(models.Block.id == f"{block_hash}{db_chain.id}")
    )
    return session.execute(query).scalar()
