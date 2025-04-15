import abc

import pydantic


class MessageBusProducerABC(abc.ABC):
    @abc.abstractmethod
    async def publish_event(self, message: pydantic.BaseModel) -> None:
        pass
