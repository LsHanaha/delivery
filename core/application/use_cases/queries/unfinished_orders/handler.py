import dataclasses

import sqlalchemy as sa

from delivery.core.domain.model.order_aggregate.order_status import OrderStatusEnum
from delivery.infrastracture.adapters.postgres.db_resource import SessionFactory
from delivery.infrastracture.adapters.postgres.tables import OrdersTable
from .models import UnfinishedOrderModel


@dataclasses.dataclass(kw_only=True)
class UnfinishedOrdersHandler:
    database_session_factory: SessionFactory

    async def collect_unfinished_orders(self) -> list[UnfinishedOrderModel]:
        async with self.database_session_factory() as session, self.database_session_factory() as session:
            result_cursor = await session.execute(
                sa.select(OrdersTable).where(OrdersTable.status != OrderStatusEnum.Completed)
            )
            return [UnfinishedOrderModel.model_validate(x) for x in result_cursor.scalars().all()]
