import abc
import uuid

from delivery.core.domain.model.courier_aggregate.courier import Courier
from delivery.core.ports.courier_repo_abc import CourierRepositoryABC
import dataclasses
from delivery.infrastracture.adapters.postgres.resource import SessionFactory


@dataclasses.dataclass(kw_only=True)
class CourierRepository(CourierRepositoryABC):
    database_session_factory: SessionFactory

    async def store_courier(self, courier: Courier) -> Courier:
        pass

    async def update_courier(self, courier: Courier) -> bool:
        pass

    async def collect_courier_by_id(self, courier_id: uuid.UUID) -> Courier | None:
        pass

    async def collect_all_free_couriers(self) -> list[Courier]:
        pass
