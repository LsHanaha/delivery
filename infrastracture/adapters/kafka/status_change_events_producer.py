import pydantic

from delivery.core.ports.message_bus_producer_abc import MessageBusProducerABC
from delivery.kafka_app import broker
from delivery.settings import settings


publisher = broker.publisher(settings.kafka_topic_status_changed)


class PublishOrderStatusChangeEvents(MessageBusProducerABC):
    async def publish_event(self, message: pydantic.BaseModel) -> None:
        await publisher.publish(message.model_dump(by_alias=True))
