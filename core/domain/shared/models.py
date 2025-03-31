import dataclasses
import random

from delivery.settings import settings


@dataclasses.dataclass(frozen=True)
class Location:
    coord_x: int
    coord_y: int

    def __composite_values__(self) -> tuple[int, int]:
        return self.coord_x, self.coord_y

    @classmethod
    def create_random_location(cls) -> "Location":
        return Location(
            coord_x=random.randint(settings.location_size_min, settings.location_size_max),
            coord_y=random.randint(settings.location_size_min, settings.location_size_max),
        )

    def calc_distance_to_another_location(self, another: "Location") -> int:
        return abs(self.coord_x - another.coord_x) + abs(self.coord_y - another.coord_y)

    def __post_init__(self) -> None:
        if not self.coord_x or not self.coord_y:
            msg = "Values must be added"
            raise ValueError(msg)
        if not 1 <= self.coord_x <= 10:
            msg = "Coord must be between 1 and 10"
            raise ValueError(msg)
        if not 1 <= self.coord_y <= 10:
            msg = "Coord must be between 1 and 10"
            raise ValueError(msg)
