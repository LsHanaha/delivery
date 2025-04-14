import random

import faker
from faststream.kafka import TestKafkaBroker
from that_depends import Provide, inject

from delivery import ioc
from delivery.core.application.use_cases.commands.assign_courier.handler import AssignCourierHandler
from delivery.core.application.use_cases.commands.create_order.handler import (
    CreateOrderCommandHandler,
    CreateOrderCommandModel,
)
from delivery.core.application.use_cases.commands.move_couriers.handler import MoveCouriersHandler
from delivery.core.domain.model.courier_aggregate.courier import Courier
from delivery.core.domain.model.courier_aggregate.transport import Transport
from delivery.core.domain.model.order_aggregate.order import Order
from delivery.core.domain.model.order_aggregate.order_status import OrderStatusEnum
from delivery.core.domain.shared.models import Location
from delivery.infrastracture.adapters.kafka.status_change_events_producer import publisher
from delivery.infrastracture.adapters.postgres.repositories.courier_repo import CourierRepository
from delivery.infrastracture.adapters.postgres.repositories.order_repo import OrderRepository
from delivery.kafka_app import broker


FAKER_OBJ = faker.Faker()


@inject
async def test_assign_courier_command(
    order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo],
    courier_repo: CourierRepository = Provide[ioc.IOCContainer.courier_repo],
    assign_courier_handler: AssignCourierHandler = Provide[ioc.IOCContainer.assign_courier_handler],
) -> None:
    amount = 5
    for _ in range(amount):
        await courier_repo.store_courier(
            Courier(
                name=FAKER_OBJ.user_name(),
                location=Location.create_random_location(),
                transport=Transport(name=FAKER_OBJ.user_name(), speed=1),
            ),
        )
        await order_repo.add_order(
            Order(
                id=FAKER_OBJ.uuid4(),
                location=Location.create_random_location(),
            ),
        )
    await courier_repo.store_courier(
        Courier(
            name=FAKER_OBJ.user_name(),
            location=Location.create_random_location(),
            transport=Transport(name=FAKER_OBJ.user_name(), speed=1),
        ),
    )
    await assign_courier_handler.handle()
    free_couriers = await courier_repo.collect_all_free_couriers()
    assert len(free_couriers) == 1

    orders = await order_repo.collect_all_assigned_orders()
    assert len(orders) == amount


@inject
async def test_create_order_command(
    order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo],
    create_order_handler: CreateOrderCommandHandler = Provide[ioc.IOCContainer.create_order_handler],
) -> None:
    new_order = CreateOrderCommandModel(BasketId=FAKER_OBJ.uuid4(), Street=FAKER_OBJ.street_name())
    await create_order_handler.handle(new_order)
    stored_order = await order_repo.collect_order_by_id(new_order.BasketId)
    assert stored_order


@inject
async def test_move_couriers_command(
    order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo],
    courier_repo: CourierRepository = Provide[ioc.IOCContainer.courier_repo],
    move_couriers_handler: MoveCouriersHandler = Provide[ioc.IOCContainer.move_couriers_handler],
) -> None:
    amount = 5
    couriers = []
    for _ in range(amount):
        created_courier = await courier_repo.store_courier(
            Courier(
                name=FAKER_OBJ.user_name(),
                location=Location(coord_x=random.randint(1, 3), coord_y=random.randint(1, 3)),
                transport=Transport(name=FAKER_OBJ.user_name(), speed=1),
            ),
        )
        couriers.append(created_courier)
        await order_repo.add_order(
            Order(
                id=FAKER_OBJ.uuid4(),
                location=Location(coord_x=random.randint(7, 9), coord_y=random.randint(7, 9)),
                courier_id=created_courier.id,
                status=OrderStatusEnum.Assigned,
            ),
        )
    await move_couriers_handler.handle()


@inject
async def test_move_couriers_with_close_order_command(
    order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo],
    courier_repo: CourierRepository = Provide[ioc.IOCContainer.courier_repo],
    move_couriers_handler: MoveCouriersHandler = Provide[ioc.IOCContainer.move_couriers_handler],
) -> None:
    async with TestKafkaBroker(broker):
        created_courier = await courier_repo.store_courier(
            Courier(
                name=FAKER_OBJ.user_name(),
                location=Location(coord_x=1, coord_y=1),
                transport=Transport(name=FAKER_OBJ.user_name(), speed=3),
            ),
        )
        await order_repo.add_order(
            Order(
                id=FAKER_OBJ.uuid4(),
                location=Location(coord_x=2, coord_y=2),
                courier_id=created_courier.id,
                status=OrderStatusEnum.Assigned,
            ),
        )
        await move_couriers_handler.handle()
        publisher.mock.assert_called_once()
