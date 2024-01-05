import base58
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic import Field

from back import storage
from shared.database import session

from back.tools.helpers import parse_cf_v1_address
from shared.types import DatumTypes, ItemTypes


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


def date_format(date: datetime) -> str:
    return str(int(date.timestamp()))


class Net(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class Chain(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    net: Net
    chain: str = Field(..., alias="name")
    count: int

    @field_validator("net")
    def check_net(cls, net: Net):
        return net.name


class ChaiWithAtoms(Chain):
    events: list['Atom'] = Field(..., alias="atoms")
    count: int = Field(exclude=True)


class Atom(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    hash: str
    date: str = Field(..., alias="created_at")

    @field_validator("date", mode="before")
    def date_format(cls, date: datetime, fields):
        return date_format(date)


class Datum(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    size: int
    version: str
    created: str = Field(..., alias="created_at")
    type: str
    data: dict = Field(..., alias="sub_datum")

    @field_validator("created", mode="before")
    def date_format(cls, date: datetime, fields):
        return date_format(date)

    @field_validator("data")
    def get_data_by_subtype(cls, data: dict, fields):
        sub_datum = {}
        if fields.data['type'] == DatumTypes.DATUM_TX:
            sub_datum['tx'] = {'hash': data['hash']}
        elif fields.data['type'] == DatumTypes.DATUM_TOKEN_EMISSION:
            data['addr'] = data['address']
            if data['type'] == "TOKEN_EMISSION_TYPE_AUTH":
                data['auth'] = data['data']
            sub_datum['token_emission'] = data

        elif fields.data['type'] == DatumTypes.DATUM_TOKEN_DECL:
            sub_datum['token_decl'] = data
        else:
            sub_datum = data
        return sub_datum


# txListLimited
class Transactions(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    transactions: list['DatumTX']


# txListLimited
class DatumTX(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    hash: str
    dateTime: str = Field(..., alias="created_at")
    token: dict = Field(..., alias="sub_datum")

    @field_validator("dateTime", mode="before")
    def date_format(cls, date: datetime, fields):
        return date_format(date)

    @field_validator("token", mode="before")
    def one_datum(cls, sub_datum: dict):
        return {"ticker": sub_datum['ticker']}


class Pkey(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    type: str
    size: int


class Sign(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    type: str
    pkey: Pkey
    pkey_hash: str
    size: int
    addr: str


class Item(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    type: str


class TxIn(Item):
    prev_hash: str
    prev_idx: int


class TxOut(Item):
    address: str
    value: str


class TxOutCond(Item):
    expires: datetime
    value: str
    subtype: str  # type

    @field_validator("expires")
    def date_format(cls, date: datetime):
        return date_format(date)


class TxSig(Item):
    size: int
    sign: Sign


class TxToken(Item):
    ticker: str
    emission_hash: str
    emission_chain_id: str


class TxOutCondSubTypeSrvStakeLock(Item):
    unlock: datetime
    value: str
    reinvest_percent: int

    @field_validator("unlock")
    def date_format(cls, date: datetime):
        return date_format(date)


# tx
class Transaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    hash: str
    token: dict = Field(..., alias="sub_datum")
    dateTime: datetime = Field(..., alias="created_at")
    in_: list[TxIn]
    # = Field(alias="in")
    out: list[TxOut]
    out_cond: list[TxOutCond]
    sig: list[TxSig]
    # token: list[TxToken]
    out_cond_srv_stake_lock: list[TxOutCondSubTypeSrvStakeLock]

    @field_validator("token", mode="before")
    def get_ticker(cls, sub_datum: dict):
        return {"ticker": sub_datum["ticker"]}

    @field_validator("dateTime")
    def date_format(cls, date: datetime):
        return date_format(date)

    @classmethod
    def model_validate(cls, *args, **kwargs):
        obj = args[0]
        obj.in_ = []
        obj.out = []
        obj.out_cond = []
        obj.sig = []
        obj.token = []
        obj.out_cond_srv_stake_lock = []
        add_to = {
            ItemTypes.TX_ITEM_TYPE_IN: obj.in_,
            ItemTypes.TX_ITEM_TYPE_OUT: obj.out,
            ItemTypes.TX_ITEM_TYPE_OUT_COND: obj.out_cond,
            ItemTypes.TX_ITEM_TYPE_SIG: obj.sig,
            ItemTypes.TX_ITEM_TYPE_IN_EMS: obj.token,
            ItemTypes.DAP_CHAIN_TX_OUT_COND_SUBTYPE_SRV_STAKE_LOCK: obj.out_cond_srv_stake_lock,
        }
        for item in obj.sub_datum["items"]:
            add_to[item['type']].append(item)
        return super().model_validate(*args, **kwargs)


# DAG
class Event(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    version: int
    round_id: int
    cell_id: str
    chain_id: int
    created: str = Field(..., alias="created_at")
    hashes: list[str]
    datum: Datum = Field(..., alias="datums")
    signs: list[dict]

    @field_validator("created", mode="before")
    def date_format(cls, date: datetime, fields):
        return date_format(date)

    @field_validator("datum", mode="before")
    def one_datum(cls, datums: list):
        return datums[0]


class Block(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    version: int
    cell_id: str
    chain_id: str | None = Field(..., alias="chainid")
    origin_chain_id: int | None = Field(..., alias="chain_id")
    created: str = Field(..., alias="created_at")
    meta: dict
    datums: list[Datum]
    signs: list[dict]

    @field_validator("created", mode="before")
    def date_format(cls, date: datetime):
        return date_format(date)


class TokenBalance(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    token: str = Field(..., alias="ticker")  # token-name
    coins: str = Field(..., alias="balance")
    datoshi: str = Field(..., alias="balance")

    @field_validator("coins")
    def calc_coins(cls, balance: int):
        return str(int(balance) / 10 ** 18)


class Wallet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    addr: str
    net: Net
    balance: list[TokenBalance] = Field(..., alias="tokens")

    @field_validator("net")
    def check_net(cls, net: Net):
        return net.name
