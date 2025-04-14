import dataclasses

from delivery.core.ports.domain_event_abc import DomainEventABC
from delivery.core.ports.message_bus_producer_abc import MessageBusProducerABC


@dataclasses.dataclass(kw_only=True)
class OrderCompletedDomainEventHandler:
    event_producer: MessageBusProducerABC

    async def handle(self, message: DomainEventABC) -> None:
        await self.event_producer.publish_event(message)
