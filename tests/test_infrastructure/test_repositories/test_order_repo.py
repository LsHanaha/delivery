import faker
from that_depends import Provide, inject

from delivery import ioc
from delivery.core.domain.model.order_aggregate.order import Order
from delivery.core.domain.model.order_aggregate.order_status import OrderStatusEnum
from delivery.core.domain.shared.models import Location
from delivery.infrastracture.adapters.postgres.repositories.order_repo import OrderRepository


FAKER_OBJ = faker.Faker()


@inject
async def test_add_order_db(
    order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo],
) -> None:
    created_order = await order_repo.add_order(
        Order(
            id=FAKER_OBJ.uuid4(),
            location=Location.create_random_location(),
        ),
    )
    assert created_order
    assert created_order.status == OrderStatusEnum.Created


@inject
async def test_fetch_order_db_by_id(order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo]) -> None:
    initial_order = await order_repo.add_order(
        Order(
            id=FAKER_OBJ.uuid4(),
            location=Location.create_random_location(),
        ),
    )
    assert initial_order

    from_db_order = await order_repo.collect_order_by_id(initial_order.id)
    assert from_db_order.id == initial_order.id


@inject
async def test_fetch_orders_db_new(order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo]) -> None:
    amount = 5
    for _ in range(amount):
        await order_repo.add_order(
            Order(
                id=FAKER_OBJ.uuid4(),
                location=Location.create_random_location(),
            ),
        )
    for _ in range(amount):
        await order_repo.add_order(
            Order(id=FAKER_OBJ.uuid4(), location=Location.create_random_location(), status=OrderStatusEnum.Assigned),
        )
    new_orders = await order_repo.collect_all_new_orders()
    assert new_orders
    assert len(new_orders) == amount
    assert all(order.status == OrderStatusEnum.Created for order in new_orders)


@inject
async def test_fetch_orders_db_assigned(order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo]) -> None:
    amount = 5
    for _ in range(amount):
        await order_repo.add_order(
            Order(
                id=FAKER_OBJ.uuid4(),
                location=Location.create_random_location(),
            ),
        )
    for _ in range(amount):
        await order_repo.add_order(
            Order(id=FAKER_OBJ.uuid4(), location=Location.create_random_location(), status=OrderStatusEnum.Assigned),
        )
    assigned_orders = await order_repo.collect_all_assigned_orders()
    assert assigned_orders
    assert len(assigned_orders) == amount
    assert all(order.status == OrderStatusEnum.Assigned for order in assigned_orders)


@inject
async def test_update_order_db(order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo]) -> None:
    initial_order = await order_repo.add_order(
        Order(
            id=FAKER_OBJ.uuid4(),
            location=Location.create_random_location(),
        ),
    )
    assert initial_order
    assert initial_order.courier_id is None

    old_location = initial_order.location
    initial_order.location = Location.create_random_location()
    res = await order_repo.update_order(initial_order)
    assert res

    updated_order = await order_repo.collect_order_by_id(initial_order.id)
    assert updated_order.id == initial_order.id
    assert old_location != updated_order.location
