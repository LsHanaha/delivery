import dataclasses
import typing

import sqlalchemy as sa

from delivery.core.application.models.outbox import OutboxEventModel
from delivery.infrastracture.adapters.postgres.db_resource import SessionFactory
from delivery.infrastracture.adapters.postgres.tables import OutboxEventsTable


@dataclasses.dataclass(kw_only=True)
class OutboxEventsRepository:
    database_session_factory: SessionFactory

    async def add_event(self, event: OutboxEventModel) -> OutboxEventModel:
        async with self.database_session_factory() as session:
            result_cursor: typing.Final[sa.Result[typing.Any]] = await session.execute(
                sa.insert(OutboxEventsTable).values(event.model_dump(exclude={"id"})).returning(OutboxEventsTable),
            )
            result: typing.Final = result_cursor.scalar_one_or_none()
            if not result:
                await session.rollback()
                msg = "Outbox event was not stored in database"
                raise ValueError(msg)
            await session.commit()
            return OutboxEventModel.model_validate(result)

    async def update_single_event(self, event: OutboxEventModel) -> OutboxEventModel:
        async with self.database_session_factory() as session:
            result_cursor: typing.Final[sa.Result[typing.Any]] = await session.execute(
                sa.update(OutboxEventsTable)
                .where(OutboxEventsTable.id == event.id)
                .values(event.model_dump())
                .returning(OutboxEventsTable),
            )
            result: typing.Final = result_cursor.scalar_one_or_none()
            if not result:
                await session.rollback()
                msg = "Outbox event was not stored in database"
                raise ValueError(msg)
            await session.commit()
            return OutboxEventModel.model_validate(result)

    async def collect_all_new_events(self) -> list[OutboxEventModel]:
        async with self.database_session_factory() as session:
            result_cursor = await session.execute(
                sa.select(OutboxEventsTable)
                .where(OutboxEventsTable.sent_at.is_(None))
                .limit(25)
                .order_by(OutboxEventsTable.id)
            )
            return [OutboxEventModel.model_validate(x) for x in result_cursor.scalars().all()]
