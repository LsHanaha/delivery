import abc
import uuid

from delivery.core.domain.model.order_aggregate.order import Order


class OrderRepositoryABC(abc.ABC):
    @abc.abstractmethod
    async def add_order(self, order: Order) -> Order:
        pass

    @abc.abstractmethod
    async def update_order(self, order: Order) -> bool:
        pass

    @abc.abstractmethod
    async def collect_order_by_id(self, order_id: uuid.UUID) -> Order | None:
        pass

    @abc.abstractmethod
    async def collect_all_new_orders(self) -> list[Order]:
        pass

    @abc.abstractmethod
    async def collect_all_assigned_orders(self) -> list[Order]:
        pass
