from datetime import datetime

from pydantic import BaseModel, field_validator

from ._common import date_format
from .datum import Datum


class Block(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    version: int
    cell_id: str
    chainid: str
    chain_id: int
    created_at: str
    meta: dict
    datums: list[Datum]
    signs: list[dict]

    @field_validator("created_at", mode="before")
    def date_format(cls, date: datetime):
        return date_format(date)
