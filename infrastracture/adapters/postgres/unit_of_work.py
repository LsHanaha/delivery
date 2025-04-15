import asyncio
import dataclasses

from delivery.core.application.domain_event_handlers.order_completed_event_handler import (
    OrderCompletedDomainEventHandler,
)
from delivery.infrastracture.adapters.postgres.db_resource import SessionFactory
from delivery.tasks_storage import TasksStorage


@dataclasses.dataclass
class UnitOfWork:
    database_session_factory: SessionFactory
    order_completed_event_handler: OrderCompletedDomainEventHandler
    tasks: list[asyncio.Task] = dataclasses.field(default_factory=list)

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def run(self, key: str | None = None) -> None:
        async with self.database_session_factory() as session:
            try:
                await session.begin()
                for task in self.tasks:
                    await task
                await session.commit()
                tasks_storage = TasksStorage()
                if tasks_storage.tasks and tasks_storage.tasks.get(key):
                    curr_tasks = tasks_storage.tasks[key]
                    for message in curr_tasks:
                        await self.order_completed_event_handler.handle(message)

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
