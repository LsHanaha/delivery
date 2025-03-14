import uuid

import pytest

from delivery.core.domain.model.courier_aggregate import transport
from delivery.core.domain.shared.models import Location


def test_compare_transports() -> None:
    first_false = transport.Transport(name="qweasd", speed=10)
    second_false = transport.Transport(name="qweasd", speed=10)
    assert first_false != second_false

    transport_id = uuid.uuid4()
    first_true = transport.Transport(id=transport_id, name="qweasd", speed=10)
    second_true = transport.Transport(id=transport_id, name="azaza", speed=20)
    assert first_true == second_true


@pytest.mark.parametrize(
    ("start", "goal", "res", "speed"),
    [
        ((2, 2), (1, 1), (1, 1), 3),
        ((1, 1), (10, 10), (10, 2), 10)
    ]
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
