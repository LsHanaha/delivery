from faststream import Depends

from delivery import ioc
from delivery.core.application.use_cases.commands.create_order.handler import CreateOrderCommandHandler
from delivery.core.application.use_cases.commands.create_order.models import CreateOrderCommandModel
from delivery.kafka_app import broker
from delivery.settings import settings


@broker.subscriber(settings.kafka_topic_basket_confirmed)
async def read_message(
    body: CreateOrderCommandModel,
    create_order_handler: CreateOrderCommandHandler = Depends(ioc.IOCContainer.create_order_handler),
) -> None:
    await create_order_handler.handle(body)
