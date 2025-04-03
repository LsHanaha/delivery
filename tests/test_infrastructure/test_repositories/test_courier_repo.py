import faker
import pytest
from that_depends import Provide, inject

from delivery import ioc
from delivery.core.domain.model.courier_aggregate.courier import Courier
from delivery.core.domain.model.courier_aggregate.courier_status import CourierStatusEnum
from delivery.core.domain.model.courier_aggregate.transport import Transport
from delivery.core.domain.shared.models import Location
from delivery.infrastracture.adapters.postgres.repositories.courier_repo import CourierRepository


FAKER_OBJ = faker.Faker()


@pytest.fixture
@inject
async def courier_creation(
    courier_repo: CourierRepository = Provide[ioc.IOCContainer.courier_repo],
) -> Courier:
    return await courier_repo.store_courier(
        Courier(
            name=FAKER_OBJ.user_name(),
            location=Location.create_random_location(),
            transport=Transport(name=FAKER_OBJ.user_name(), speed=1),
        ),
    )


async def test_add_courier_db(courier_creation: Courier) -> None:
    assert courier_creation
    assert courier_creation.status == CourierStatusEnum.Free


@inject
async def test_fetch_courier_by_id_db(
    courier_creation: Courier,
    courier_repo: CourierRepository = Provide[ioc.IOCContainer.courier_repo],
) -> None:
    assert courier_creation
    stored = await courier_repo.collect_courier_by_id(courier_creation.id)

    assert stored
    assert stored.id == courier_creation.id
    assert stored.transport == courier_creation.transport


@inject
async def test_fetch_free_couriers_db(
    courier_repo: CourierRepository = Provide[ioc.IOCContainer.courier_repo],
) -> None:
    amount = 5
    for _ in range(amount):
        await courier_repo.store_courier(
            Courier(
                name=FAKER_OBJ.user_name(),
                location=Location.create_random_location(),
                transport=Transport(name=FAKER_OBJ.user_name(), speed=1),
                status=CourierStatusEnum.Free,
            ),
        )
        await courier_repo.store_courier(
            Courier(
                name=FAKER_OBJ.user_name(),
                location=Location.create_random_location(),
                transport=Transport(name=FAKER_OBJ.user_name(), speed=1),
                status=CourierStatusEnum.Busy,
            ),
        )

    free_couriers = await courier_repo.collect_all_free_couriers()
    assert free_couriers
    assert len(free_couriers) == amount
    assert all(courier.status == CourierStatusEnum.Free for courier in free_couriers)


@inject
async def test_update_courier_db(
    courier_creation: Courier,
    courier_repo: CourierRepository = Provide[ioc.IOCContainer.courier_repo],
) -> None:
    assert courier_creation
    courier_creation.location = Location.create_random_location()
    courier_creation.assign_busy()
    courier_creation.transport.speed = 1
    res = await courier_repo.update_courier(courier_creation)
    assert res

    stored_courier = await courier_repo.collect_courier_by_id(courier_creation.id)
    assert stored_courier.status == CourierStatusEnum.Busy
    assert stored_courier.transport.speed == courier_creation.transport.speed
    assert stored_courier.location == courier_creation.location
