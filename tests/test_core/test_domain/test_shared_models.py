import pydantic
import pytest

from delivery.core.domain.shared import models
from delivery.settings import settings


def test_location_model_distance() -> None:
    first_path = models.Location(coord_x=1, coord_y=10).calc_distance_to_another_location(
        models.Location(coord_x=10, coord_y=1)
    )
    second_path = models.Location(coord_x=10, coord_y=1).calc_distance_to_another_location(
        models.Location(coord_x=1, coord_y=10)
    )
    assert first_path == second_path

    assert (
        models.Location(coord_x=1, coord_y=1).calc_distance_to_another_location(models.Location(coord_x=1, coord_y=1))
        == 0
    )


def test_location_random() -> None:
    for _ in range(10):
        location = models.Location.create_random_location()
        assert location
        assert settings.location_size_min <= location.coord_x <= settings.location_size_max
        assert settings.location_size_min <= location.coord_y <= settings.location_size_max


def test_location_create_errors() -> None:
    with pytest.raises(pydantic.ValidationError):
        models.Location(coord_x=0, coord_y=1)
    with pytest.raises(pydantic.ValidationError):
        models.Location(coord_x=1, coord_y=0)
    with pytest.raises(pydantic.ValidationError):
        models.Location(coord_x=-1, coord_y=1)
    with pytest.raises(pydantic.ValidationError):
        models.Location(coord_x=-1, coord_y=1)

    val = models.Location(coord_x=1, coord_y=1)
    with pytest.raises(pydantic.ValidationError):
        val.coord_x = 2
    with pytest.raises(pydantic.ValidationError):
        val.coord_y = 2
