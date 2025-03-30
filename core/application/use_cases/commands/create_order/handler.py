import dataclasses

from delivery.core.domain.model.order_aggregate.order import Order
from delivery.infrastracture.adapters.postgres.repositories.order_repo import OrderRepository
from .models import CreateOrderCommandModel


@dataclasses.dataclass
class CreateOrderCommandHandler:
    order_repo: OrderRepository

    async def handle(self, new_oder: CreateOrderCommandModel) -> None:
        order = Order(id=new_oder.BasketId, location=new_oder.Street)
        await self.order_repo.add_order(order)
