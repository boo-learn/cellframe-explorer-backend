from pydantic import BaseModel


class Net(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    id: int
    name: str