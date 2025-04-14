import faker
import pytest
from that_depends import Provide, inject

from delivery import ioc
from delivery.core.domain.shared.models import Location
from delivery.infrastracture.adapters.grpc.geo_location import GeoLocation


FAKER_OBJ = faker.Faker()


@pytest.mark.parametrize(
    "pair",
    [
        {"name": "Тестировочная", "location": Location(coord_x=1, coord_y=1)},
        {"name": "Бажная", "location": Location(8, 8)},
    ],
)
@inject
async def test_geo_location_known(
    pair: dict[str, str | Location],
    geo_location_service: GeoLocation = Provide[ioc.IOCContainer.geo_location_service],
) -> None:
    got_location = await geo_location_service.collect_location_by_street_name(pair["name"])
    assert got_location
    assert got_location == pair["location"]
