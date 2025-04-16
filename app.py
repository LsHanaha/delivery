import asyncio
import typing
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from that_depends import Provide, inject

from delivery import ioc
from delivery.api.adapters.http_ad.views import ROUTER_OBJ
from delivery.api.adapters.kafka.basket_confirmed.consumer import broker
from delivery.periodic_tasks import OutboxPatternJob


@asynccontextmanager
@inject
async def lifespan(
    app_: FastAPI, periodic_tasks: OutboxPatternJob = Provide[ioc.IOCContainer.periodic_tasks]
) -> typing.AsyncContextManager[None]:
    await broker.start()
    task = asyncio.create_task(periodic_tasks.run())
    yield
    await broker.close()
    task.cancel()


app = FastAPI(docs_url="/", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ROUTER_OBJ, prefix="/api/v1", tags=["use-cases"])
