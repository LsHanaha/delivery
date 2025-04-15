import asyncio
import dataclasses

from delivery.infrastracture.adapters.postgres.repositories.courier_repo import CourierRepository
from delivery.infrastracture.adapters.postgres.repositories.order_repo import OrderRepository
from delivery.infrastracture.adapters.postgres.unit_of_work import UnitOfWork


@dataclasses.dataclass(kw_only=True)
class MoveCouriersHandler:
    courier_repo: CourierRepository
    order_repo: OrderRepository
    unit_of_work_handler: UnitOfWork

    async def handle(self) -> None:
        assigned_orders = await self.order_repo.collect_all_assigned_orders()
        for order in assigned_orders:
            courier = await self.courier_repo.collect_courier_by_id(order.courier_id)
            if not courier:
                raise ValueError(f"No courier found for order {order.id}")
            courier.move(order.location)
            if courier.location == order.location:
                courier.assign_free()
                order.close_order()

            async with self.unit_of_work_handler as uow:
                uow.tasks.append(asyncio.create_task(self.courier_repo.update_courier(courier)))
                uow.tasks.append(asyncio.create_task(self.order_repo.update_order(order)))
                await uow.run(order.id)
