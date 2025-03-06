import pydantic
import pytest

from delivery.core.domain.shared import models


def test_location_model_distance() -> None:
    first_path = models.Location(coord_x=1, coord_y=10).calc_distance_to_another_location(
        models.Location(coord_x=10, coord_y=1)
    )
    second_path = models.Location(coord_x=10, coord_y=1).calc_distance_to_another_location(
        models.Location(coord_x=1, coord_y=10)
    )
    assert first_path == second_path

    assert models.Location(coord_x=1, coord_y=1).calc_distance_to_another_location(
        models.Location(coord_x=1, coord_y=1)
    ) == 0


def test_location_random() -> None:
    for _ in range(10):
        location = models.Location.create_random_location()
        assert location
        assert 1 <= location.coord_x <= 10
        assert 1 <= location.coord_y <= 10


def test_location_create_errors() -> None:
    with pytest.raises(pydantic.ValidationError):
        models.Location(coord_x=0, coord_y=1)
    with pytest.raises(pydantic.ValidationError):
        models.Location(coord_x=1, coord_y=0)
    with pytest.raises(pydantic.ValidationError):
        models.Location(coord_x=-1, coord_y=1)
    with pytest.raises(pydantic.ValidationError):
        models.Location(coord_x=-1, coord_y=1)
    with pytest.raises(pydantic.ValidationError):
        val = models.Location(coord_x=1, coord_y=1)
        val.coord_x = 2
        val.coord_y = 2
