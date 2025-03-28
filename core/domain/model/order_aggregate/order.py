import pydantic

from delivery.core.domain.model.order_aggregate.order_status import OrderStatusEnum
from delivery.core.domain.shared.models import Location


class Order(pydantic.BaseModel):
    id: pydantic.UUID4
    location: Location
    status: OrderStatusEnum = OrderStatusEnum.Created
    courier_id: pydantic.UUID4 | None = None

    def assign_courier(self, courier_id: pydantic.UUID4) -> None:
        if not courier_id:
            msg = "Order. Courier id must bet non-null value"
            raise ValueError(msg)
        if self.status != OrderStatusEnum.Created:
            raise ValueError(f"Order. Cannot assign new courier for an order. We already have one {self.courier_id=}")
        self.courier_id = courier_id
        self.status = OrderStatusEnum.Assigned

    def close_order(self) -> None:
        if not self.courier_id or self.status != OrderStatusEnum.Assigned:
            msg = "Order. Cannot close non-assigned order"
            raise ValueError(msg)
        self.status = OrderStatusEnum.Completed

    model_config = pydantic.ConfigDict(from_attributes=True)
