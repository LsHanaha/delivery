import typing

import fastapi
from fastapi import Depends

from delivery import ioc
from delivery.core.application.use_cases.commands.assign_courier.handler import AssignCourierHandler
from delivery.core.application.use_cases.commands.move_couriers.handler import MoveCouriersHandler
from delivery.core.application.use_cases.queries.busy_couriers.handler import BusyCouriersHandler
from delivery.core.application.use_cases.queries.busy_couriers.models import BusyCourierModel
from delivery.core.application.use_cases.queries.unfinished_orders.handler import UnfinishedOrdersHandler
from delivery.core.application.use_cases.queries.unfinished_orders.models import UnfinishedOrderModel


ROUTER_OBJ: typing.Final = fastapi.APIRouter()


@ROUTER_OBJ.get("/couriers/")
async def get_all_busy_couriers(
    busy_couriers_handler: typing.Annotated[BusyCouriersHandler, Depends(ioc.IOCContainer.busy_couriers_handler)],
) -> list[BusyCourierModel]:
    return await busy_couriers_handler.collect_busy_couriers()


@ROUTER_OBJ.get("/orders/active/")
async def get_all_unfinished_orders(
    unfinished_orders_handler: typing.Annotated[
        UnfinishedOrdersHandler, Depends(ioc.IOCContainer.unfinished_orders_handler)
    ],
) -> list[UnfinishedOrderModel]:
    return await unfinished_orders_handler.collect_unfinished_orders()


@ROUTER_OBJ.post(
    "/couriers/assign/",
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def assign_courier(
    assign_courier_handler: typing.Annotated[AssignCourierHandler, Depends(ioc.IOCContainer.assign_courier_handler)],
) -> bool:
    await assign_courier_handler.handle()
    return True


@ROUTER_OBJ.post("/couriers/move/", status_code=fastapi.status.HTTP_201_CREATED)
async def move_couriers(
    move_couriers_handler: typing.Annotated[MoveCouriersHandler, Depends(ioc.IOCContainer.move_couriers_handler)],
) -> bool:
    await move_couriers_handler.handle()
    return True
