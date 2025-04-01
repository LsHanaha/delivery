import faker
from that_depends import Provide, inject

from delivery import ioc
from delivery.core.application.use_cases.queries.busy_couriers.handler import BusyCouriersHandler
from delivery.core.application.use_cases.queries.unfinished_orders.handler import UnfinishedOrdersHandler
from delivery.core.domain.model.courier_aggregate.courier import Courier
from delivery.core.domain.model.courier_aggregate.courier_status import CourierStatusEnum
from delivery.core.domain.model.courier_aggregate.transport import Transport
from delivery.core.domain.model.order_aggregate.order import Order
from delivery.core.domain.model.order_aggregate.order_status import OrderStatusEnum
from delivery.core.domain.shared.models import Location
from delivery.infrastracture.adapters.postgres.repositories.courier_repo import CourierRepository
from delivery.infrastracture.adapters.postgres.repositories.order_repo import OrderRepository


FAKER_OBJ = faker.Faker()


@inject
async def test_unfinished_orders_query(
    order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo],
    unfinished_orders_handler: UnfinishedOrdersHandler = Provide[ioc.IOCContainer.unfinished_orders_handler],
) -> None:
    amount = 5
    for _ in range(amount):
        await order_repo.add_order(
            Order(
                id=FAKER_OBJ.uuid4(),
                location=Location.create_random_location(),
            ),
        )
        await order_repo.add_order(
            Order(id=FAKER_OBJ.uuid4(), location=Location.create_random_location(), status=OrderStatusEnum.Assigned),
        )
        await order_repo.add_order(
            Order(id=FAKER_OBJ.uuid4(), location=Location.create_random_location(), status=OrderStatusEnum.Completed),
        )

    unfinished_orders = await unfinished_orders_handler.collect_unfinished_orders()
    assert unfinished_orders
    assert len(unfinished_orders) == amount * 2


@inject
async def test_busy_couriers_query(
    courier_repo: CourierRepository = Provide[ioc.IOCContainer.courier_repo],
    busy_couriers_handler: BusyCouriersHandler = Provide[ioc.IOCContainer.busy_couriers_handler],
) -> None:
    amount = 5
    for _ in range(amount):
        await courier_repo.store_courier(
            Courier(
                name=FAKER_OBJ.user_name(),
                location=Location.create_random_location(),
                transport=Transport(name=FAKER_OBJ.user_name(), speed=1),
                status=CourierStatusEnum.Free,
            ),
        )
        await courier_repo.store_courier(
            Courier(
                name=FAKER_OBJ.user_name(),
                location=Location.create_random_location(),
                transport=Transport(name=FAKER_OBJ.user_name(), speed=1),
                status=CourierStatusEnum.Busy,
            ),
        )

    busy_couriers = await busy_couriers_handler.collect_busy_couriers()
    assert busy_couriers
    assert len(busy_couriers) == amount
