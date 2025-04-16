import asyncio
import dataclasses

from delivery.core.application.models.outbox import OutboxEventModel
from delivery.core.domain.model.order_aggregate.domain_events.order_completed_domain_event import (
    OrderCompletedDomainEvent,
)
from delivery.domain_events_storage import DomainEventStorage
from delivery.infrastracture.adapters.postgres.db_resource import SessionFactory
from delivery.infrastracture.adapters.postgres.repositories.outbox_repo import OutboxEventsRepository
from delivery.settings import settings


@dataclasses.dataclass
class UnitOfWork:
    database_session_factory: SessionFactory
    outbox_events_repo: OutboxEventsRepository
    tasks: list[asyncio.Task] = dataclasses.field(default_factory=list)

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def run(self, key: str | None = None) -> None:
        async with self.database_session_factory() as session:
            try:
                await session.begin()
                for task in self.tasks:
                    await task
                domain_events_storage = DomainEventStorage()
                if domain_events_storage.tasks and domain_events_storage.tasks.get(key):
                    curr_events = domain_events_storage.tasks[key]
                    for event in curr_events:
                        if isinstance(event, OrderCompletedDomainEvent):
                            await self.outbox_events_repo.add_event(
                                OutboxEventModel(event=event.model_dump(), topic=settings.kafka_topic_basket_confirmed)
                            )
                await session.commit()

            except Exception as exc:
                await session.rollback()
                msg = "Got an error"
                raise ValueError(msg) from exc
            finally:
                await session.close()

    async def __aexit__(self, *args) -> None:  # noqa: ANN002
        if not self.database_session_factory:
            return
        async with self.database_session_factory() as session:
            await session.close()
