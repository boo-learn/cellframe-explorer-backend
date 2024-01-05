import json
from starlette.datastructures import QueryParams
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException

import storage
from schemas import serializers
from schemas.validators import valid_wallet_address


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
    wallet_schema = serializers.Wallet.model_validate(wallet)
    return wallet_schema.model_dump_json(indent=4)

