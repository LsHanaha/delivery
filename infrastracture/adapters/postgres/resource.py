import dataclasses
from delivery.settings import settings
import typing
from delivery.infrastracture.adapters.postgres.db_dsn import build_db_dsn
from sqlalchemy.ext import asyncio as sa_async


def engine_factory() -> typing.AsyncIterator[sa_async.AsyncEngine]:
    url: typing.Final = build_db_dsn(
        db_dsn=settings.db_dsn,
        database_name=settings.database_name,
        drivername="postgresql+asyncpg",
    )
    engine = sa_async.create_async_engine(url, echo=True)
    yield engine
    engine.dispose()


@dataclasses.dataclass()
class SessionFactory:
    session_maker: sa_async.async_sessionmaker[sa_async.AsyncSession]

    def __call__(self) -> sa_async.AsyncSession:
        return self.session_maker()


async def create_session_factory(engine: sa_async.AsyncEngine) -> typing.AsyncIterator[SessionFactory]:
    session_maker: typing.Final = sa_async.async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )
    yield SessionFactory(session_maker)
