import pytest
from delivery.infrastracture.adapters.postgres.tables import Base
from delivery.infrastracture.adapters.postgres.db_dsn import build_db_dsn
from delivery.settings import settings
import typing
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
async def database():
    url: typing.Final = build_db_dsn(
        settings.db_dsn,
        database_name=settings.database_name,
        drivername="postgresql+asyncpg",
    )
    engine = sa.create_engine(url)

    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
async def db_session(database):
    connection = database.connect()
    transaction = connection.begin()

    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()