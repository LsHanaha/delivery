import typing

import pytest
import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker

from delivery.infrastracture.adapters.postgres.db_dsn import build_db_dsn
from delivery.infrastracture.adapters.postgres.tables import Base
from delivery.settings import settings
from delivery import ioc
import sqlalchemy.ext.asyncio as sa_async
from delivery.infrastracture.adapters.postgres.resource import SessionFactory


@pytest.fixture(autouse=True)
async def _mock_ioc_container() -> typing.AsyncIterator[None]:
    engine: typing.Final = await ioc.IOCContainer.database_resource()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    connection: typing.Final = await engine.connect()
    transaction: typing.Final = await connection.begin()
    session_maker: typing.Final[sa_async.async_sessionmaker[sa_async.AsyncSession]] = sa_async.async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        autoflush=False,
    )
    await connection.begin_nested()
    ioc.IOCContainer.database_session_factory.override(SessionFactory(session_maker))
    try:
        yield
    finally:
        if connection.in_transaction():
            await transaction.rollback()
        await connection.close()

        ioc.IOCContainer.reset_override()
        await ioc.IOCContainer.tear_down()


# @pytest.fixture(scope="session", autouse=True)
# async def database() -> sa.Engine:
#     print("AZAZAZ LALKA")
#     url: typing.Final = build_db_dsn(
#         settings.db_dsn,
#         database_name=settings.database_name,
#         drivername="postgresql+asyncpg",
#     )
#     engine = sa.create_engine(url)
#     Base.metadata.create_all(engine)
#     yield engine
#     Base.metadata.drop_all(engine)
#
#
# @pytest.fixture(autouse=True)
# async def db_session(database: sa.Engine) -> Session:
#     connection = database.connect()
#     transaction = connection.begin()
#
#     session = sessionmaker(bind=connection)()
#
#     yield session
#
#     session.close()
#     transaction.rollback()
#     connection.close()
