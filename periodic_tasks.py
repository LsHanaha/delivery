import asyncio
import dataclasses

from delivery.core.application.domain_event_handlers.order_completed_event_handler import (
    OrderCompletedDomainEventHandler,
)
from delivery.core.domain.model.order_aggregate.domain_events.order_completed_domain_event import (
    OrderCompletedDomainEvent,
)
from delivery.infrastracture.adapters.postgres.repositories.outbox_repo import OutboxEventsRepository
from delivery.settings import settings


@dataclasses.dataclass(kw_only=True)
class OutboxPatternJob:
    outbox_events_repo: OutboxEventsRepository
    order_completed_event_handler: OrderCompletedDomainEventHandler

    async def run(self) -> None:
        while True:
            new_events = await self.outbox_events_repo.collect_all_new_events()
            for event in new_events:
                if event.topic == settings.kafka_topic_basket_confirmed:
                    await self.order_completed_event_handler.handle(
                        OrderCompletedDomainEvent.model_validate(event.event)
                    )
                    event.mark_as_sent()
                    await self.outbox_events_repo.update_single_event(event)
            await asyncio.sleep(settings.outbox_job_period_s)
