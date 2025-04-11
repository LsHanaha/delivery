import typing

import grpc
from grpc import Channel

from delivery.infrastracture.adapters.grpc import GeoContract_pb2_grpc
from delivery.settings import settings


async def create_grpc_resource() -> typing.AsyncIterator[GeoContract_pb2_grpc.GeoStub]:
    channel: Channel = grpc.aio.insecure_channel(settings.geo_dsn)
    stub = GeoContract_pb2_grpc.GeoStub(channel)
    yield stub
    await channel.close()
