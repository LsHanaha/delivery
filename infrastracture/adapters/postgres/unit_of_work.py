import asyncio
import dataclasses

from sqlalchemy.ext.asyncio import AsyncSession


@dataclasses.dataclass
class UnitOfWork:
    session: AsyncSession
    tasks: list[asyncio.Task] = dataclasses.field(default_factory=list)

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def run(self) -> None:
        try:
            await self.session.begin()
            for task in self.tasks:
                await task
        except Exception as exc:
            await self.session.rollback()
            await self.session.close()
            msg = "Got an error"
            raise ValueError(msg) from exc
        finally:
            await self.session.close()

    async def __aexit__(self, *args) -> None:  # noqa: ANN002
        if not self.session:
            return
        await self.session.commit()
        await self.session.close()
