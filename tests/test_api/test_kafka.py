import typing

from faker import Faker
from faststream.kafka import TestKafkaBroker
from that_depends import Provide, inject

from delivery import ioc
from delivery.api.adapters.kafka.basket_confirmed.consumer import broker
from delivery.core.application.use_cases.commands.create_order.models import CreateOrderCommandModel
from delivery.infrastracture.adapters.postgres.repositories.order_repo import OrderRepository
from delivery.settings import settings


FAKER_OBJ: typing.Final = Faker()


@inject
async def test_kafka_create_order(
    order_repo: OrderRepository = Provide[ioc.IOCContainer.order_repo],
) -> None:
    async with TestKafkaBroker(broker) as br:
        order_model = CreateOrderCommandModel(BasketId=FAKER_OBJ.uuid4(), Street=FAKER_OBJ.street_name())
        await br.publish(order_model.model_dump(), topic=settings.kafka_topic_basket_confirmed)
        stored_order = await order_repo.collect_order_by_id(order_model.BasketId)
        assert stored_order
