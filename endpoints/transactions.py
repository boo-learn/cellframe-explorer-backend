import json

from starlette.datastructures import QueryParams
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from pydantic import TypeAdapter

from schemas import serializers
import storage
from shared.database import models
from tools.helpers import to_dict, to_json


# hhttp.add("txListLimited", workTx.http_handler_list)
def tx_list_limited(query: QueryParams, session: Session):
    DEFAULT_PAGE_SIZE = 10
    net_name = query.get("net")
    if net_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'net'")

    count = int(query.get('count', DEFAULT_PAGE_SIZE))
    page = int(query.get('page', 1))
    reverse = not (bool(query.get('reverse', None) and query.get('reverse') == 'true'))
    print(reverse)
    limit = count
    offset = (page - 1) * limit

    datums_tx = storage.datum.get_datums_tx(session, net_name, limit, offset, reverse)

    return serializers.Transactions.model_validate({"transactions": datums_tx}).model_dump_json()


# hhttp.add("txListCount", workTx.http_handler_list_count)
def list_count(query: QueryParams, session: Session):
    net_name = query.get("net")
    if net_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'net'")

    db_net = storage.net.get_net_by_name(session, name=net_name)
    if not db_net:
        return json.dumps(
            {
                "code": 30,
                "error": f"Can't search network with name: {net_name}"
            },
            indent=4)

    count = storage.datum.count_datums_tx(session, net_name)
    return json.dumps({
        "net": net_name,
        "countTx": str(count)
    })


# hhttp.add("tx", workTx.http_handler_tx)
def get_datum_tx(query: QueryParams, session: Session):
    net_name = query.get("net")
    if net_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'net'")

    hash = query.get('hash')
    if hash is None:
        raise HTTPException(status_code=400, detail="Required query-param 'hash'")

    db_net = storage.net.get_net_by_name(session, name=net_name)
    if not db_net:
        return json.dumps(
            {
                "code": 30,
                "error": f"Can't search network with name: {net_name}"
            },
            indent=4)

    datum_tx = storage.datum.get_datum_tx(session, net_name, hash)
    if datum_tx is None:
        return json.dumps({
            "code": 20,
            "error": f"Can't items for transaction with hash: {hash}"
        })

    return serializers.Transaction.model_validate(datum_tx).model_dump_json(indent=4)
