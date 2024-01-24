from starlette.datastructures import QueryParams
from sqlalchemy.orm import Session


def error_500(query: QueryParams, session: Session):
    10 / 0
    return "complete"