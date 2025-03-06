import random

import pydantic


class Location(pydantic.BaseModel):
    coord_x: int = pydantic.Field(..., ge=1, le=10, frozen=True)
    coord_y: int = pydantic.Field(..., ge=1, le=10, frozen=False)

    @classmethod
    def create_random_location(cls) -> "Location":
        return Location(coord_x=random.randint(1, 10), coord_y=random.randint(1, 10))

    def calc_distance_to_another_location(self, another: "Location") -> int:
        return abs(self.coord_x - another.coord_x) + abs(self.coord_y - another.coord_y)
