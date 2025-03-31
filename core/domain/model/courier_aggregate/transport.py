import uuid

import pydantic

from delivery.core.domain.shared import models


class Transport(pydantic.BaseModel):
    id: pydantic.UUID4 | None = pydantic.Field(default_factory=lambda: uuid.uuid4(), frozen=True)
    name: str
    speed: int = pydantic.Field(ge=1, le=3)

    def move(self, start: models.Location, goal: models.Location) -> models.Location:
        if start == goal:
            return start

        dist_x = goal.coord_x - start.coord_x
        dist_y = goal.coord_y - start.coord_y
        dist_can_travel = self.speed

        if dist_x > 0:
            new_x = min(start.coord_x + dist_can_travel, goal.coord_x)
        else:
            new_x = max(start.coord_x - dist_can_travel, goal.coord_x)

        dist_can_travel -= abs(dist_x)
        new_y = start.coord_y
        if dist_can_travel > 0:
            if dist_y > 0:
                new_y = min(start.coord_y + dist_can_travel, goal.coord_y)
            else:
                new_y = max(start.coord_y - dist_can_travel, goal.coord_y)
        return models.Location(coord_x=new_x, coord_y=new_y)

    def __eq__(self, other: "Transport") -> bool:
        return self.id == other.id

    model_config = pydantic.ConfigDict(from_attributes=True)
