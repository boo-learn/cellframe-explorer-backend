from sqlalchemy import select, func
from sqlalchemy.orm import Session, lazyload, subqueryload, selectinload

from shared.database import models
from logger import logIt


def get_chain(session: Session, net_name: str, chain_name: str) -> models.Chain | None:
    return (
        session.execute(
            select(models.Chain)
            .where(
                (models.Chain.name == chain_name) & (models.Net.name == net_name)
            )
            # .join(models.Atom)
        )
    ).scalar()

# def get_chain(session: Session, net_name: str, chain_name: str) -> models.Chain | None:
#     return (
#         session.execute(
#             select(models.Chain)
#             .where(
#                 (models.Chain.name == chain_name) & (models.Net.name == net_name)
#             )
#             .join(models.Atom)
#         )
#     ).scalar()

