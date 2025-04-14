from that_depends import BaseContainer, providers

from delivery.core.application.domain_event_handlers.order_completed_event_handler import (
    OrderCompletedDomainEventHandler,
)
from delivery.core.application.use_cases.commands.assign_courier.handler import AssignCourierHandler
from delivery.core.application.use_cases.commands.create_order.handler import CreateOrderCommandHandler
from delivery.core.application.use_cases.commands.move_couriers.handler import MoveCouriersHandler
from delivery.core.application.use_cases.queries.busy_couriers.handler import BusyCouriersHandler
from delivery.core.application.use_cases.queries.unfinished_orders.handler import UnfinishedOrdersHandler
from delivery.core.domain.services.dispatch_service import DispatchService
from delivery.infrastracture.adapters.grpc.geo_location import GeoLocation
from delivery.infrastracture.adapters.grpc.grpc_resource import create_grpc_resource
from delivery.infrastracture.adapters.kafka.status_change_events_producer import PublishOrderStatusChangeEvents
from delivery.infrastracture.adapters.postgres.db_resource import create_session_factory, engine_factory
from delivery.infrastracture.adapters.postgres.repositories.courier_repo import CourierRepository
from delivery.infrastracture.adapters.postgres.repositories.order_repo import OrderRepository
from delivery.infrastracture.adapters.postgres.unit_of_work import UnitOfWork


class IOCContainer(BaseContainer):
    database_resource = providers.Resource(engine_factory)
    grpc_resource = providers.Resource(create_grpc_resource)

    database_session_factory = providers.Resource(
        create_session_factory,
        engine=database_resource.cast,
    )
    dispatch_service = providers.Singleton(DispatchService)

    # INFRA
    geo_location_service = providers.Factory(GeoLocation, grpc_connection=grpc_resource.cast)
    event_producer = providers.Factory(PublishOrderStatusChangeEvents)
    order_completed_event_handler = providers.Factory(
        OrderCompletedDomainEventHandler, event_producer=event_producer.cast
    )

    unit_of_work = providers.Factory(
        UnitOfWork,
        database_session_factory=database_session_factory.cast,
        order_completed_event_handler=order_completed_event_handler.cast,
    )

    # REPOS
    order_repo = providers.Factory(OrderRepository, database_session_factory=database_session_factory.cast)
    courier_repo = providers.Factory(CourierRepository, database_session_factory=database_session_factory.cast)

    # USE CASES
    busy_couriers_handler = providers.Factory(
        BusyCouriersHandler, database_session_factory=database_session_factory.cast
    )
    unfinished_orders_handler = providers.Factory(
        UnfinishedOrdersHandler, database_session_factory=database_session_factory.cast
    )
    assign_courier_handler = providers.Factory(
        AssignCourierHandler,
        courier_repo=courier_repo.cast,
        order_repo=order_repo.cast,
        dispatch_service=dispatch_service.cast,
    )
    create_order_handler = providers.Factory(
        CreateOrderCommandHandler,
        order_repo=order_repo.cast,
        geo_location_service=geo_location_service.cast,
    )
    move_couriers_handler = providers.Factory(
        MoveCouriersHandler,
        courier_repo=courier_repo.cast,
        order_repo=order_repo.cast,
        unit_of_work_handler=unit_of_work.cast,
    )
