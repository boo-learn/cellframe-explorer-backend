import base58

import storage
from shared.database import session
from tools.helpers import parse_cf_v1_address


def validate_v1_address(net_name: str, address: str) -> bool:
    try:
        version, net_id, sign_id, public_hash, summary_hash, control_hash = parse_cf_v1_address(address)
    except (ValueError, IndexError):
        return False

    with session() as db_session:
        net = storage.net.get_net_by_id(db_session, net_id)

    if net is None or net_name != net.name:
        return False

    return True


def valid_wallet_address(net_name, address: str) -> bool:
    versions = {
        1: validate_v1_address
    }

    try:
        version = base58.b58decode(address)[0]
    except (ValueError, IndexError):
        return False
    try:
        return versions[version](net_name, address)
    except KeyError:
        return False
