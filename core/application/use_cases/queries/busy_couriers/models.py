import pydantic

from delivery.core.domain.shared.models import Location


class BusyCourierLocationModel(pydantic.BaseModel):
    X: int
    Y: int


class BusyCourierModel(pydantic.BaseModel):
    Id: pydantic.UUID4 = pydantic.Field(..., alias="id")
    Name: str = pydantic.Field(..., alias="name")
    location: Location

    @pydantic.computed_field(alias="Location")
    def courier_location(self) -> BusyCourierLocationModel:
        return BusyCourierLocationModel(X=self.location.coord_x, Y=self.location.coord_y)

    model_config = pydantic.ConfigDict(from_attributes=True)
