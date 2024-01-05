import json

from back import storage
from back import schemas

from starlette.datastructures import QueryParams
from sqlalchemy.orm import Session

from fastapi.exceptions import HTTPException

from back.schemas import valid_wallet_address


# hhttp.add("w_addr", walletInfo)
def get_wallet(query: QueryParams, session: Session):
    address = query.get("addr")
    if address is None:
        raise HTTPException(status_code=400, detail="Required query-param 'address'")
    net_name = query.get("net")
    if net_name is None:
        raise HTTPException(status_code=400, detail="Required query-param 'net'")
    if not valid_wallet_address(net_name, address):
        return json.dumps({
            "error": {
                "code": 24,
                "msg": f"Invalid address {address}"
            }
        }, indent=4)

    wallet = storage.wallet.get_wallet_by_address(session, address)
    if wallet is None:
        raise HTTPException(status_code=404, detail=f"Wallet with address={address} not found")
    wallet_schema = schemas.Wallet.model_validate(wallet)
    return wallet_schema.model_dump_json(indent=4)

# def get_info(query: QueryParams, session: Session):
#     print(f"get info {query=}")
#     return {"handler": "get_info", "query": query}
#
#
# def get_net_by_id(query: QueryParams, session: Session):
#     net_id = query["net_id"]
#     net_db: models.Net = session.scalar(select(models.Net).where(models.Net.id == net_id))
#     if net_db is None:
#         raise HTTPException(status_code=404, detail=f"Net with id={net_id} not found")
#     return {"id": net_db.id, "name": net_db.name}
