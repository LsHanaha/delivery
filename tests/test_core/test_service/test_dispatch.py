import faker
import pytest

from delivery.core.domain.model.courier_aggregate.courier import Courier
from delivery.core.domain.model.courier_aggregate.courier_status import CourierStatusEnum
from delivery.core.domain.model.courier_aggregate.transport import Transport
from delivery.core.domain.model.order_aggregate.order import Order
from delivery.core.domain.model.order_aggregate.order_status import OrderStatusEnum
from delivery.core.domain.services.dispatch_service import DispatchService
from delivery.core.domain.shared.models import Location


FAKER_OBJ = faker.Faker()


def test_dispatch_bad_routes() -> None:
    bad_order = Order(id=FAKER_OBJ.uuid4(), location=Location.create_random_location(), status=OrderStatusEnum.Assigned)
    couriers = [
        Courier(
            name=FAKER_OBJ.user_name(),
            transport=Transport(name=FAKER_OBJ.user_name(), speed=2),
            location=Location.create_random_location(),
            status=CourierStatusEnum.Busy,
        ),
        Courier(
            name=FAKER_OBJ.user_name(),
            transport=Transport(name=FAKER_OBJ.user_name(), speed=2),
            location=Location.create_random_location(),
            status=CourierStatusEnum.Busy,
        ),
    ]
    with pytest.raises(ValueError):
        DispatchService().dispatch(bad_order, couriers)

    good_order = Order(id=FAKER_OBJ.uuid4(), location=Location.create_random_location(), status=OrderStatusEnum.Created)
    with pytest.raises(ValueError):
        DispatchService().dispatch(good_order, couriers)


def test_select_nearest() -> None:
    order_location = Location(coord_x=1, coord_y=1)
    closest_location = Location(coord_x=2, coord_y=1)

    couriers = [
        Courier(
            name=FAKER_OBJ.user_name(),
            transport=Transport(name=FAKER_OBJ.user_name(), speed=2),
            location=Location.create_random_location(),
            status=CourierStatusEnum.Free,
        )
        for _ in range(5)
    ]
    couriers[0].location = closest_location
    selected_unit = DispatchService().dispatch(
        Order(id=FAKER_OBJ.uuid4(), location=order_location, status=OrderStatusEnum.Created), couriers
    )
    assert selected_unit == couriers[0]
