import random

import pydantic

from delivery.settings import settings


class Location(pydantic.BaseModel):
    coord_x: int = pydantic.Field(..., ge=settings.location_size_min, le=settings.location_size_max, frozen=True)
    coord_y: int = pydantic.Field(..., ge=settings.location_size_min, le=settings.location_size_max, frozen=True)

    @classmethod
    def create_random_location(cls) -> "Location":
        return Location(
            coord_x=random.randint(settings.location_size_min, settings.location_size_max),
            coord_y=random.randint(settings.location_size_min, settings.location_size_max),
        )

    def calc_distance_to_another_location(self, another: "Location") -> int:
        return abs(self.coord_x - another.coord_x) + abs(self.coord_y - another.coord_y)
