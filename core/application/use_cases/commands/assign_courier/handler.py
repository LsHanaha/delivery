import dataclasses

from delivery.core.domain.services.dispatch_service import DispatchService
from delivery.infrastracture.adapters.postgres.repositories.courier_repo import CourierRepository
from delivery.infrastracture.adapters.postgres.repositories.order_repo import OrderRepository


@dataclasses.dataclass(kw_only=True)
class AssignCourierHandler:
    courier_repo: CourierRepository
    order_repo: OrderRepository
    dispatch_service: DispatchService

    async def handle(self) -> None:
        free_couriers = await self.courier_repo.collect_all_free_couriers()
        new_orders = await self.order_repo.collect_all_new_orders()

        if not free_couriers:
            msg = "No free couriers available"
            raise ValueError(msg)

        for order in new_orders:
            selected_courier = self.dispatch_service.dispatch(order, free_couriers)
            if not selected_courier:
                raise ValueError(f"Can not dispatch courier for order {order.id=}")
            selected_courier.assign_busy()
            order.assign_courier(selected_courier.id)

            await self.courier_repo.update_courier(selected_courier)
            await self.order_repo.update_order(order)
            free_couriers.remove(selected_courier)
