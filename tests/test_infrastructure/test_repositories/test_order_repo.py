import typing

from that_depends import Provide, inject

from delivery import ioc
from delivery.infrastracture.adapters.postgres.repositories.order_repo import OrderRepository
from delivery.core.domain.model.order_aggregate.order import Order
from delivery.core.domain.model.order_aggregate.order_status import OrderStatusEnum
from delivery.core.domain.shared.models import Location
import faker


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
