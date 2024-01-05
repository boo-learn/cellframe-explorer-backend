from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query,
    Request,
    Response
)

from fastapi.exceptions import HTTPException
from starlette.datastructures import QueryParams
from sqlalchemy.orm import Session

from back.core.const import (
    EXPLORER_URL,
    EXPLORER_TAGS
)

from back.endpoints import (
    wallets, dags, transactions, blocks
)

from back.core import depends

router = APIRouter(prefix="/expl", tags=EXPLORER_TAGS)


def get_query_handler(query: QueryParams, session: Session):
    try:
        method = query["method"]
    except KeyError:
        raise HTTPException(status_code=400, detail="Required query-param 'method'")
    handlers = {
        "w_addr": wallets.get_wallet,
        "dagListCount": dags.dag_list_count,
        "dagListLimited": dags.dag_list_limited,
        "dag": dags.dag_info,
        "txListLimited": transactions.tx_list_limited,
        "txListCount": transactions.list_count,
        "tx": transactions.get_datum_tx,
        # "txValidation": txs.tx_validation,
        "blockListLimited": blocks.block_list,
        "blockListCount": dags.dag_list_count, # Yes, It's duplicate
        "block": blocks.get_block,
    }
    try:
        handler = handlers[method]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"method={method} not supported")
    return handler(query, session)


@router.get("")
def entry_point(request: Request, session: Session = Depends(depends.sync_db_session)):
    query = request.query_params
    return Response(content=get_query_handler(query, session), media_type="json")
