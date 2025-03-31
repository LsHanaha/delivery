import abc
import uuid

from delivery.core.domain.model.courier_aggregate.courier import Courier


class CourierRepositoryABC(abc.ABC):
    @abc.abstractmethod
    async def store_courier(self, courier: Courier) -> Courier:
        pass

    @abc.abstractmethod
    async def update_courier(self, courier: Courier) -> bool:
        pass

    @abc.abstractmethod
    async def collect_all_free_couriers(self) -> list[Courier]:
        pass

    @abc.abstractmethod
    async def collect_courier_by_id(self, courier_id: uuid.UUID) -> Courier | None:
        pass
