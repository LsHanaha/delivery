import typing

import httpx
import pytest
from faker import Faker
from fastapi import status
from that_depends import Provide, inject

from delivery import ioc
from delivery.core.domain.model.courier_aggregate.courier import Courier, Location, Transport
from delivery.core.domain.model.courier_aggregate.courier_status import CourierStatusEnum
from delivery.core.domain.model.order_aggregate.order import Order, OrderStatusEnum
from delivery.infrastracture.adapters.postgres.repositories.courier_repo import CourierRepository
from delivery.infrastracture.adapters.postgres.repositories.order_repo import OrderRepository


FAKER_OBJ: typing.Final = Faker()


@pytest.mark.parametrize("amount", [5, 0])
@inject
async def test_get_all_busy_couriers_view(
    amount: int,
    async_client: httpx.AsyncClient,
    courier_repo: CourierRepository = Provide[ioc.IOCContainer.courier_repo],
) -> None:
    for _ in range(amount):
        await courier_repo.store_courier(
            Courier(
                name=FAKER_OBJ.user_name(),
                location=Location.create_random_location(),
                transport=Transport(name=FAKER_OBJ.user_name(), speed=1),
                status=CourierStatusEnum.Busy,
            ),
        )

    response: typing.Final = await async_client.get("/api/v1/couriers/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == amount


@pytest.mark.parametrize("amount", [5, 0])
@inject
async def test_get_all_unfinished_orders_view(
    amount: int,
    async_client: httpx.AsyncClient,
    order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo],
) -> None:
    for _ in range(amount):
        await order_repo.add_order(
            Order(id=FAKER_OBJ.uuid4(), location=Location.create_random_location(), status=OrderStatusEnum.Assigned),
        )

    response: typing.Final = await async_client.get("/api/v1/orders/active/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == amount


@inject
async def test_assign_couriers_view(
    async_client: httpx.AsyncClient,
    order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo],
    courier_repo: CourierRepository = Provide[ioc.IOCContainer.courier_repo],
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

    response: typing.Final = await async_client.post("/api/v1/couriers/assign/")
    assert response.status_code == status.HTTP_201_CREATED
    free_couriers = await courier_repo.collect_all_free_couriers()
    assert len(free_couriers) == 1

    orders = await order_repo.collect_all_assigned_orders()
    assert len(orders) == amount


@inject
async def test_move_couriers_view(
    async_client: httpx.AsyncClient,
    order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo],
    courier_repo: CourierRepository = Provide[ioc.IOCContainer.courier_repo],
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

    response_assign: typing.Final = await async_client.post("/api/v1/couriers/assign/")
    assert response_assign.status_code == status.HTTP_201_CREATED
    response_move: typing.Final = await async_client.post("/api/v1/couriers/move/")
    assert response_move.status_code == status.HTTP_201_CREATED
