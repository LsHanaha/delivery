import pydantic


class BusyCourierLocationModel(pydantic.BaseModel):
    X: int = pydantic.Field(..., alias="coord_x")
    Y: int = pydantic.Field(..., alias="coord_y")


class BusyCourierModel(pydantic.BaseModel):
    Id: pydantic.UUID4 = pydantic.Field(..., alias="id")
    Name: str = pydantic.Field(..., alias="name")
    Location: BusyCourierLocationModel = pydantic.Field(..., alias="location")
    TransportId: pydantic.UUID4 | None = pydantic.Field(..., alias="transport_id")
