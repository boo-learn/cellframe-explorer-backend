import json

from starlette.datastructures import QueryParams
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from pydantic import TypeAdapter

from back import schemas
from back import storage
from shared.database import models
from shared.types import ChainTypes
from back.tools.helpers import to_dict, to_json


# hhttp.add("blockListLimited", workBlock.http_handler_block_list)
def block_list(query: QueryParams, session: Session):
    DEFAULT_PAGE_SIZE = 10
    net_name = query.get("net")
    if net_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'net'")

    chain_name = query.get("chain")
    if chain_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'chain'")

    count = int(query.get('count', DEFAULT_PAGE_SIZE))
    page = int(query.get('page', 1))
    reverse = bool(query.get('reverse', None) and query.get('reverse') == 'true')

    limit = count
    offset = (page - 1) * limit

    db_blocks = storage.block.get_blocks(
        session, net_name, chain_name,
        limit=limit, offset=offset, reverse=reverse
    )

    return json.dumps({
        "net": net_name,
        "chain": chain_name,
        "blocks": to_dict(db_blocks, schema=schemas.Atom)
    })


# hhttp.add("block", workBlock.http_handler_block)
def get_block(query: QueryParams, session: Session):
    net_name = query.get("net")
    if net_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'net'")
    chain_name = query.get("chain")
    if chain_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'chain'")
    hash = query.get('hash')
    if hash is None:
        raise HTTPException(status_code=400, detail="Required query-param 'hash'")

    block = storage.block.get_block(session, net_name, chain_name, hash)
    block_schema = schemas.Block.model_validate(block)
    return block_schema.model_dump_json(indent=4)