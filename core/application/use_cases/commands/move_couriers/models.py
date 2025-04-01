import pydantic


class UnfinishedOrderLocationModel(pydantic.BaseModel):
    X: int = pydantic.Field(..., alias="coord_x")
    Y: int = pydantic.Field(..., alias="coord_y")


class UnfinishedOrderModel(pydantic.BaseModel):
    Id: pydantic.UUID4 = pydantic.Field(..., alias="Id")
    Location: UnfinishedOrderLocationModel = pydantic.Field(..., alias="location")
