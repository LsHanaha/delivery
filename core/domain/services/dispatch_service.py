from abc import ABC, abstractmethod

from delivery.core.domain.model.courier_aggregate.courier import Courier
from delivery.core.domain.model.courier_aggregate.courier_status import CourierStatusEnum
from delivery.core.domain.model.order_aggregate.order import Order
from delivery.core.domain.model.order_aggregate.order_status import OrderStatusEnum


class DispatchServiceABC(ABC):
    @abstractmethod
    def dispatch(self, order: Order, candidates: list[Courier]) -> Courier:
        pass


class DispatchService(DispatchServiceABC):
    def dispatch(self, order: Order, candidates: list[Courier]) -> Courier:
        if order.status != OrderStatusEnum.Created:
            raise ValueError(f"Order {order.id=} is in process or completed. Can't be assigned for a new courier")

        free_couriers = [candid8 for candid8 in candidates if candid8.status == CourierStatusEnum.Free]
        if not free_couriers:
            raise ValueError(f"No free courier for an order {order.id=}")

        the_fastest = free_couriers[0]
        fastest_time = free_couriers[0].calculate_steps_to_target(order.location)
        for unit in free_couriers[1:]:
            unit_time = unit.calculate_steps_to_target(order.location)
            if unit.calculate_steps_to_target(order.location) < fastest_time:
                the_fastest = unit
                fastest_time = unit_time

        return the_fastest
