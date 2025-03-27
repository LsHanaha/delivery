import uuid

from delivery.core.ports.order_repo_abc import OrderRepositoryABC
from delivery.core.domain.model.order_aggregate.order import Order
from delivery.core.domain.shared.models import Location
from delivery.core.domain.model.order_aggregate.order_status import OrderStatusEnum

import typing

import dataclasses

import sqlalchemy as sa

from delivery.infrastracture.adapters.postgres.resource import SessionFactory
from delivery.infrastracture.adapters.postgres.tables import OrdersTable
from delivery.infrastracture.adapters.postgres.repositories import shared


@dataclasses.dataclass(kw_only=True)
class OrderRepository(OrderRepositoryABC):
    database_session_factory: SessionFactory

    @staticmethod
    def _convert_one_entity_from_db(db_order: OrdersTable) -> Order:
        return Order(
            id=db_order.id,
            location=shared.location_from_db_format(db_order.location),
            status=db_order.status,
            courier_id=db_order.courier_id
        )

    @staticmethod
    def _convert_one_entity_for_db(order: Order) -> dict:
        return {**order.model_dump(exclude={"location"}), "location": shared.location_to_db_format(order.location)}

    async def add_order(self, order: Order) -> Order:
        async with self.database_session_factory() as session:
            result_cursor: typing.Final[sa.Result[typing.Any]] = await session.execute(
                sa.insert(OrdersTable).values(**self._convert_one_entity_for_db(order)).returning(OrdersTable),
            )
            result: typing.Final = result_cursor.scalar_one_or_none()
            await session.commit()
            return Order.model_validate(result)

    async def update_order(self, order: Order) -> bool:
        async with self.database_session_factory() as session:
            result_cursor: typing.Final[sa.Result[typing.Any]] = await session.execute(
                sa.update(OrdersTable)
                .where(OrdersTable.id == order.id)
                .values(
                    **self._convert_one_entity_for_db(order)
                )
                .returning(1),
            )
            await session.commit()
            return bool(result_cursor.scalar_one_or_none())

    async def collect_all_new_orders(self) -> list[Order]:
        async with self.database_session_factory() as session:
            result_cursor = await session.execute(
                sa.select(OrdersTable).where(OrdersTable.status == OrderStatusEnum.Created)
            )
            return [self._convert_one_entity_from_db(x) for x in result_cursor.scalars().all()]

    async def collect_all_assigned_orders(self) -> list[Order]:
        async with self.database_session_factory() as session:
            result_cursor = await session.execute(
                sa.select(OrdersTable).where(OrdersTable.status == OrderStatusEnum.Created)
            )
            return [self._convert_one_entity_from_db(x) for x in result_cursor.scalars().all()]

    async def collect_order_by_id(self, order_id: uuid.UUID) -> Order | None:
        async with self.database_session_factory() as session:
            result_cursor = await session.execute(
                sa.select(OrdersTable).where(OrdersTable.id == order_id)
            )
            result: typing.Final = result_cursor.scalar_one_or_none()
            if not result:
                return None
            return self._convert_one_entity_from_db(result)
