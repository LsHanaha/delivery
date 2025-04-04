import pydantic
from delivery.core.domain.shared.models import Location


class UnfinishedOrderLocationModel(pydantic.BaseModel):
    X: int
    Y: int


class UnfinishedOrderModel(pydantic.BaseModel):
    Id: pydantic.UUID4 = pydantic.Field(..., alias="id")
    location: Location = pydantic.Field(exclude=True)

    @pydantic.computed_field(alias="Location")
    def unfinished_location(self) -> UnfinishedOrderLocationModel:
        return UnfinishedOrderLocationModel(X=self.location.coord_x, Y=self.location.coord_y)

    model_config = pydantic.ConfigDict(from_attributes=True, populate_by_name=True)
