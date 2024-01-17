from pydantic import BaseModel

from .net import Net


class Chain(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    id: int
    net: Net
    name: str
