import random
import uuid

import faker
import pytest

from delivery.core.domain.model.courier_aggregate import courier_status, transport
from delivery.core.domain.model.courier_aggregate.courier import Courier
from delivery.core.domain.shared.models import Location


FAKER_OBJ = faker.Faker()


def _create_random_transport(speed: int | None = None) -> transport.Transport:
    return transport.Transport(name=FAKER_OBJ.user_name(), speed=speed if speed else random.randint(1, 3))


def test_compare_transports() -> None:
    first_false = transport.Transport(name="qweasd", speed=2)
    second_false = transport.Transport(name="qweasd", speed=2)
    assert first_false != second_false

    transport_id = uuid.uuid4()
    first_true = transport.Transport(id=transport_id, name="qweasd", speed=3)
    second_true = transport.Transport(id=transport_id, name="azaza", speed=3)
    assert first_true == second_true


@pytest.mark.parametrize(
    ("start", "goal", "res", "speed"), [((2, 2), (1, 1), (1, 1), 3), ((1, 1), (10, 10), (4, 1), 3)]
)
def test_move_transport(start: tuple, goal: tuple, res: tuple, speed: int) -> None:
    start_x, start_y = start
    goal_x, goal_y = goal
    res_x, res_y = res

    start = Location(coord_x=start_x, coord_y=start_y)
    goal = Location(coord_x=goal_x, coord_y=goal_y)
    car = transport.Transport(name="car", speed=speed)
    res = car.move(start, goal)
    assert res == Location(coord_x=res_x, coord_y=res_y)


def test_create_courier() -> None:
    new_courier = Courier(
        name=FAKER_OBJ.first_name(), transport=_create_random_transport(), location=Location.create_random_location()
    )
    assert new_courier.transport
    assert new_courier.location
    assert new_courier.status == courier_status.CourierStatusEnum.Free


def test_change_statuses() -> None:
    new_courier = Courier(
        name=FAKER_OBJ.first_name(), transport=_create_random_transport(), location=Location.create_random_location()
    )
    assert new_courier.status == courier_status.CourierStatusEnum.Free
    new_courier.assign_busy()
    assert new_courier.status == courier_status.CourierStatusEnum.Busy
    new_courier.assign_free()
    assert new_courier.status == courier_status.CourierStatusEnum.Free


def test_calculate_steps() -> None:
    new_courier = Courier(
        name=FAKER_OBJ.first_name(),
        transport=_create_random_transport(speed=2),
        location=Location(coord_x=1, coord_y=1),
    )
    target_location = Location(coord_x=5, coord_y=5)
    assert new_courier.calculate_steps_to_target(target_location) == 4

    target_location = Location(coord_x=5, coord_y=6)
    assert new_courier.calculate_steps_to_target(target_location) == 5


def test_move_one_step() -> None:
    new_courier = Courier(
        name=FAKER_OBJ.first_name(),
        transport=_create_random_transport(speed=2),
        location=Location(coord_x=1, coord_y=1),
    )
    target_location = Location(coord_x=5, coord_y=5)
    new_courier.move(target_location)
    assert new_courier.location == Location(coord_x=3, coord_y=1)
