import pydantic

from delivery.core.domain.model.order_aggregate.order_status import OrderStatusEnum
from delivery.core.ports.domain_event_abc import DomainEventABC


class OrderCompletedDomainEvent(DomainEventABC):
    order_id: pydantic.UUID4 = pydantic.Field(..., serialization_alias="orderId")
    order_status: OrderStatusEnum = pydantic.Field(..., serialization_alias="orderStatus")
