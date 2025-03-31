from that_depends import BaseContainer, providers

from delivery.infrastracture.adapters.postgres.db_resource import create_session_factory, engine_factory
from delivery.infrastracture.adapters.postgres.repositories.courier_repo import CourierRepository
from delivery.infrastracture.adapters.postgres.repositories.order_repo import OrderRepository


class IOCContainer(BaseContainer):
    database_resource = providers.Resource(engine_factory)
    database_session_factory = providers.Resource(
        create_session_factory,
        engine=database_resource.cast,
    )
    order_repo = providers.Factory(OrderRepository, database_session_factory=database_session_factory.cast)
    courier_repo = providers.Factory(CourierRepository, database_session_factory=database_session_factory.cast)
