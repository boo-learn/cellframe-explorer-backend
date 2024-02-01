import json

from starlette.datastructures import QueryParams
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException

from pycfhelpers.common.types import ChainTypes
from schemas import serializers
import storage


# hhttp.add("dagListCount", workDag.http_handler_dag_list_count)
def dag_list_count(query: QueryParams, session: Session):
    net_name = query.get("net")
    if net_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'net'")

    chain_name = query.get("chain")
    if chain_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'chain'")

    chain = storage.chain.get_chain(session, net_name, chain_name)
    if chain is None:
        raise HTTPException(status_code=404, detail=f"Chain with name={chain_name} in net={net_name} not found")
    chain_schema = serializers.Chain.model_validate(chain)
    # print(f"{chain_schema=}")
    return chain_schema.model_dump_json(indent=4)


# hhttp.add("dagListLimited", workDag.http_handler_dag_list_limited)
def dag_list_limited(query: QueryParams, session: Session):
    DEFAULT_PAGE_SIZE = 10
    net_name = query.get("net")
    if net_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'net'")

    chain_name = query.get("chain")
    if chain_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'chain'")

    db_chain = storage.chain.get_chain(session, net_name=net_name, chain_name=chain_name)
    if not db_chain:
        return json.dumps({
            "error": {
                "code": 23,
                "msg": f"Failed to get chain named {chain_name}."
            }
        }, indent=4)
    if db_chain.type != ChainTypes.dag_poa:
        return json.dumps({
            "error": {
                "msg": f"Chain={chain_name} is not DAG"
            }
        }, indent=4)

    count = int(query.get('count', DEFAULT_PAGE_SIZE))
    page = int(query.get('page', 1))
    reverse = not (bool(query.get('reverse', None) and query.get('reverse') == 'old'))

    limit = count
    offset = (page - 1) * limit
    if db_chain.type == ChainTypes.esbocs:
        current_storage = storage.block.get_blocks
    elif db_chain.type == ChainTypes.dag_poa:
        current_storage = storage.event.get_events
    else:
        raise TypeError
    atoms = current_storage(session, net_name, chain_name, limit=limit, offset=offset, reverse=reverse)
    db_chain.atoms = atoms
    chain_schema = serializers.ChaiWithAtoms.model_validate(db_chain)
    return chain_schema.model_dump_json(indent=4)


# hhttp.add("dag", workDag.http_handler_dag_info)
def dag_info(query: QueryParams, session: Session):
    net_name = query.get("net")
    if net_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'net'")

    chain_name = query.get("chain")
    if chain_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'chain'")

    hash = query.get("hash")
    if hash is None:
        raise HTTPException(status_code=400, detail="Required query-param 'hash'")

    chain = storage.chain.get_chain(session, net_name, chain_name)
    if chain is None:
        raise HTTPException(status_code=404, detail=f"Chain with name={chain_name} in net={net_name} not found")

    # DAG == Event
    db_event = storage.event.get_event(session, net_name, chain_name, event_hash=hash)
    if db_event is None:
        raise HTTPException(status_code=404, detail=f"Event with hash ={hash} not found")
    # print(f"{db_event.version=}")
    # print(f"{type(db_event.version)=}")
    event_schema = serializers.Event.model_validate(db_event)
    return event_schema.model_dump_json(indent=4)

