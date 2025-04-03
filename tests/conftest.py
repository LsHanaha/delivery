import typing

import pytest
import sqlalchemy.ext.asyncio as sa_async
from fastapi.testclient import TestClient

from delivery import ioc
from delivery.app import app
from delivery.infrastracture.adapters.postgres.db_resource import SessionFactory
from delivery.infrastracture.adapters.postgres.tables import Base


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


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)
