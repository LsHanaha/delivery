import uuid

import faker

from delivery.core.domain.model.order_aggregate import order, order_status
from delivery.core.domain.shared.models import Location


FAKER_OBJ = faker.Faker()


def test_create_order() -> None:
    new_order = order.Order(id=uuid.uuid4(), name=FAKER_OBJ.name(), location=Location.create_random_location())
    assert new_order.id
    assert new_order.status == order_status.OrderStatusEnum.Created


def test_assign_courier() -> None:
    new_order = order.Order(id=uuid.uuid4(), name=FAKER_OBJ.name(), location=Location.create_random_location())
    assert new_order.courier_id is None
    new_order.assign_courier(FAKER_OBJ.uuid4())
    assert new_order.courier_id is not None
    assert new_order.status == order_status.OrderStatusEnum.Assigned


def test_close_order() -> None:
    new_order = order.Order(id=uuid.uuid4(), name=FAKER_OBJ.name(), location=Location.create_random_location())
    new_order.assign_courier(FAKER_OBJ.uuid4())
    assert new_order.status == order_status.OrderStatusEnum.Assigned
    new_order.close_order()
    assert new_order.status == order_status.OrderStatusEnum.Completed
