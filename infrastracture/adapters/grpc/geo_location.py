import dataclasses

from delivery.core.domain.shared.models import Location
from delivery.core.ports.geo_location_abc import GeoLocationABC
from delivery.infrastracture.adapters.grpc import GeoContract_pb2, GeoContract_pb2_grpc


@dataclasses.dataclass(kw_only=True)
class GeoLocation(GeoLocationABC):
    grpc_connection: GeoContract_pb2_grpc.GeoStub

    async def collect_location_by_street_name(self, street: str) -> Location:
        response = await self.grpc_connection.GetGeolocation(GeoContract_pb2.GetGeolocationRequest(Street=street))
        result = response.ListFields()[0][1]
        return Location(coord_x=result.x, coord_y=result.y)
