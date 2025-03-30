import dataclasses

import sqlalchemy as sa

from delivery.core.domain.model.courier_aggregate.courier_status import CourierStatusEnum
from delivery.infrastracture.adapters.postgres.db_resource import SessionFactory
from delivery.infrastracture.adapters.postgres.tables import CouriersTable
from .models import BusyCourierModel


@dataclasses.dataclass(kw_only=True)
class BusyCouriersHandler:
    database_session_factory: SessionFactory

    async def collect_busy_couriers(self) -> list[BusyCourierModel]:
        async with self.database_session_factory() as session:
            result_cursor = await session.execute(
                sa.select(CouriersTable).where(CouriersTable.status == CourierStatusEnum.Busy)
            )
            return [BusyCourierModel.model_validate(x) for x in result_cursor.scalars().all()]
