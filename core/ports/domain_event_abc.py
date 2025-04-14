import abc

import pydantic


class DomainEventABC(abc.ABC, pydantic.BaseModel):
    event_id: pydantic.UUID4 | None = pydantic.Field(None, serialization_alias="eventId")
