from pydantic import BaseModel, field_validator
from datetime import datetime
from ._common import date_format


class Datum(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    size: int
    version: str
    created_at: str
    type: str
    sub_datum: dict

    @field_validator("created_at", mode="before")
    def date_format(cls, date: datetime, fields):
        return date_format(date)
