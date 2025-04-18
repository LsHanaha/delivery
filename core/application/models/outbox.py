import datetime
import typing

import pydantic


class OutboxEventModel(pydantic.BaseModel):
    id: int | None = None
    event: dict[str, typing.Any]
    topic: str
    created_at: datetime.datetime = datetime.datetime.now(tz=datetime.UTC)
    sent_at: datetime.datetime | None = None

    def mark_as_sent(self) -> None:
        self.sent_at = datetime.datetime.now(tz=datetime.UTC)

    model_config = pydantic.ConfigDict(from_attributes=True)
