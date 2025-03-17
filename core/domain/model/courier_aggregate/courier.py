import math
import uuid

import pydantic
from delivery.core.domain.model.courier_aggregate.courier_status import CourierStatusEnum
from delivery.core.domain.model.courier_aggregate.transport import Transport
from delivery.core.domain.shared.models import Location


class Courier(pydantic.BaseModel):
    id: pydantic.UUID4 = pydantic.Field(default_factory=lambda: uuid.uuid4(), frozen=True)
    name: str
    transport: Transport
    location: Location
    status: CourierStatusEnum = CourierStatusEnum.Free

    def assign_busy(self) -> None:
        self.status = CourierStatusEnum.Busy

    def assign_free(self) -> None:
        self.status = CourierStatusEnum.Free

    def calculate_steps_to_target(self, target_location: Location) -> int:
        return math.ceil(self.location.calc_distance_to_another_location(target_location) / self.transport.speed)

    def move(self, target_location: Location) -> None:
        self.location = self.transport.move(self.location, target_location)
