import dataclasses
import typing
import uuid

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import insert as pg_insert

from delivery.core.domain.model.courier_aggregate.courier import Courier
from delivery.core.domain.model.courier_aggregate.courier_status import CourierStatusEnum
from delivery.core.ports.courier_repo_abc import CourierRepositoryABC
from delivery.infrastracture.adapters.postgres.db_resource import SessionFactory
from delivery.infrastracture.adapters.postgres.tables import CouriersTable, TransportsTable


@dataclasses.dataclass(kw_only=True)
class CourierRepository(CourierRepositoryABC):
    database_session_factory: SessionFactory

    @staticmethod
    def _make_format_to_store(courier: Courier) -> CouriersTable:
        return CouriersTable(
            id=courier.id,
            name=courier.name,
            location=courier.location,
            status=courier.status,
            transport_id=courier.transport.id,
            transport=TransportsTable(
                id=courier.transport.id, name=courier.transport.name, speed=courier.transport.speed
            ),
        )

    async def store_courier(self, courier: Courier) -> Courier:
        async with self.database_session_factory() as session:
            db_courier = self._make_format_to_store(courier)
            session.add(db_courier)
            await session.flush()
            await session.refresh(db_courier, ["transport"])
            if not db_courier:
                await session.rollback()
                msg = "Courier was not stored in database"
                raise ValueError(msg)
            await session.commit()
            return Courier.model_validate(db_courier)

    async def update_courier(self, courier: Courier) -> bool:
        async with self.database_session_factory() as session:
            stored_courier = await session.execute(
                sa.update(CouriersTable)
                .where(CouriersTable.id == courier.id)
                .values(**{**courier.model_dump(exclude={"transport", "location"}), "location": courier.location})
                .returning(CouriersTable)
            )
            if courier.transport:
                await session.execute(
                    pg_insert(TransportsTable)
                    .values(**courier.transport.model_dump())
                    .on_conflict_do_update(index_elements=[TransportsTable.id], set_=courier.transport.model_dump())
                )
            await session.commit()
            return bool(stored_courier.scalar_one_or_none())

    async def collect_courier_by_id(self, courier_id: uuid.UUID) -> Courier | None:
        async with self.database_session_factory() as session:
            result_cursor = await session.execute(
                sa.select(CouriersTable)
                .where(CouriersTable.id == courier_id)
                .options(orm.selectinload(CouriersTable.transport))
            )
            result: typing.Final = result_cursor.scalar_one_or_none()
            if not result:
                return None
            return Courier.model_validate(result)

    async def collect_all_free_couriers(self) -> list[Courier]:
        async with self.database_session_factory() as session:
            result_cursor = await session.execute(
                sa.select(CouriersTable)
                .where(CouriersTable.status == CourierStatusEnum.Free)
                .options(orm.selectinload(CouriersTable.transport))
            )
            if not result_cursor:
                return []
            return [Courier.model_validate(x) for x in result_cursor.scalars().all()]
