import dataclasses

from delivery.core.domain.model.order_aggregate.order import Order
from delivery.core.domain.shared.models import Location
from delivery.core.ports.geo_location_abc import GeoLocationABC
from delivery.infrastracture.adapters.postgres.repositories.order_repo import OrderRepository
from .models import CreateOrderCommandModel


@dataclasses.dataclass
class CreateOrderCommandHandler:
    order_repo: OrderRepository
    geo_location_service: GeoLocationABC

    async def _fetch_location(self, street_name: str) -> Location:
        return await self.geo_location_service.collect_location_by_street_name(street_name)

    async def handle(self, new_oder: CreateOrderCommandModel) -> None:
        location = await self._fetch_location(new_oder.Street)
        order = Order(id=new_oder.BasketId, location=location)
        await self.order_repo.add_order(order)
