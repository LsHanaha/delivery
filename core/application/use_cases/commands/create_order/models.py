import pydantic


class CreateOrderCommandModel(pydantic.BaseModel):
    BasketId: pydantic.UUID4
    Street: str
