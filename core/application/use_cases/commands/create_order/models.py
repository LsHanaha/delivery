import pydantic

from delivery.core.domain.shared.models import Location


class CreateOrderCommandModel(pydantic.BaseModel):
    BasketId: pydantic.UUID4
    Street: Location
