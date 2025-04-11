import abc

from delivery.core.domain.shared.models import Location


class GeoLocationABC(abc.ABC):
    @abc.abstractmethod
    async def collect_location_by_street_name(self, street_name: str) -> Location:
        pass
