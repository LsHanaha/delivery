import typing
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from delivery.api.adapters.http_ad.views import ROUTER_OBJ
from delivery.api.adapters.kafka.basket_confirmed.consumer import broker


@asynccontextmanager
async def lifespan(app_: FastAPI) -> typing.AsyncContextManager[None]:  # noqa:ARG001
    await broker.start()
    yield
    await broker.close()


app = FastAPI(docs_url="/", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ROUTER_OBJ, prefix="/api/v1", tags=["use-cases"])
