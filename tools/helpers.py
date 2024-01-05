import base58
import hashlib
from typing import Any
from pydantic import BaseModel, TypeAdapter
# from schemas.sign import *



def parse_cf_v1_address(address: str) -> tuple[int, int, int, bytes, bytes, bytes]:
    bdata: bytes = base58.b58decode(address)
    version = bdata[0]
    net_id = int.from_bytes((bdata[1:9]), byteorder='little')
    sign_id = int.from_bytes((bdata[9:13]), byteorder='little')
    public_hash = bdata[13:45]
    control_hash = bdata[45:]
    hash = hashlib.sha3_256()
    hash.update(bdata[:45])
    summary_hash = hash.digest()
    if summary_hash != control_hash:
        raise ValueError(f"Address={address} not valid")
    return version, net_id, sign_id, public_hash, summary_hash, control_hash

def to_dict(objects: list[Any], schema: type[BaseModel]) -> list[dict]:
    adapter = TypeAdapter(list[schema])
    return adapter.dump_python(adapter.validate_python(objects))


def to_json(objects: list[Any], schema: type[BaseModel], indent=4) -> bytes:
    adapter = TypeAdapter(list[schema])
    return adapter.dump_json(adapter.validate_python(objects), indent=indent)