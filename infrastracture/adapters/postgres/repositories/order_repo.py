import dataclasses
import typing
import uuid

import sqlalchemy as sa

from delivery.core.domain.model.order_aggregate.order import Order
from delivery.core.domain.model.order_aggregate.order_status import OrderStatusEnum
from delivery.core.ports.order_repo_abc import OrderRepositoryABC
from delivery.infrastracture.adapters.postgres.db_resource import SessionFactory
from delivery.infrastracture.adapters.postgres.tables import OrdersTable


@dataclasses.dataclass(kw_only=True)
class OrderRepository(OrderRepositoryABC):
    database_session_factory: SessionFactory

    async def add_order(self, order: Order) -> Order:
        async with self.database_session_factory() as session:
            result_cursor: typing.Final[sa.Result[typing.Any]] = await session.execute(
                sa.insert(OrdersTable)
                .values(**{**order.model_dump(exclude={"location"}), "location": order.location})
                .returning(OrdersTable),
            )
            result: typing.Final = result_cursor.scalar_one_or_none()
            if not result:
                await session.rollback()
                msg = "Order was not stored in database"
                raise ValueError(msg)
            await session.commit()
            return Order.model_validate(result)

    async def update_order(self, order: Order) -> bool:
        async with self.database_session_factory() as session:
            result_cursor: typing.Final[sa.Result[typing.Any]] = await session.execute(
                sa.update(OrdersTable)
                .where(OrdersTable.id == order.id)
                .values(**{**order.model_dump(exclude={"location"}), "location": order.location})
                .returning(1),
            )
            await session.commit()
            return bool(result_cursor.scalar_one_or_none())

    async def collect_all_new_orders(self) -> list[Order]:
        async with self.database_session_factory() as session:
            result_cursor = await session.execute(
                sa.select(OrdersTable).where(OrdersTable.status == OrderStatusEnum.Created)
            )
            return [Order.model_validate(x) for x in result_cursor.scalars().all()]

    async def collect_all_assigned_orders(self) -> list[Order]:
        async with self.database_session_factory() as session:
            result_cursor = await session.execute(
                sa.select(OrdersTable).where(OrdersTable.status == OrderStatusEnum.Assigned)
            )
            return [Order.model_validate(x) for x in result_cursor.scalars().all()]

    async def collect_order_by_id(self, order_id: uuid.UUID) -> Order | None:
        async with self.database_session_factory() as session:
            result_cursor = await session.execute(sa.select(OrdersTable).where(OrdersTable.id == order_id))
            result: typing.Final = result_cursor.scalar_one_or_none()
            if not result:
                return None
            return Order.model_validate(result)
