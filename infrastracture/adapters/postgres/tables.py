import typing
import uuid

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects import postgresql


METADATA: typing.Final = sa.MetaData()
Base = orm.declarative_base(metadata=METADATA)


class TransportsTable(Base):
    __tablename__ = "transports"

    id: orm.Mapped[typing.Annotated[uuid.UUID, orm.mapped_column(postgresql.UUID(as_uuid=True), primary_key=True)]]
    name: orm.Mapped[typing.Annotated[str, orm.mapped_column(sa.String, nullable=False)]]
    speed: orm.Mapped[typing.Annotated[int, orm.mapped_column(sa.Integer, nullable=False)]]


class CouriersTable(Base):
    __tablename__ = "couriers"
    __allow_unmapped__ = True

    id: orm.Mapped[typing.Annotated[uuid.UUID, orm.mapped_column(postgresql.UUID(as_uuid=True), primary_key=True)]]
    name: orm.Mapped[typing.Annotated[str, orm.mapped_column(sa.String, nullable=False)]]
    transport_id: orm.Mapped[
        typing.Annotated[
            uuid.UUID, orm.mapped_column(postgresql.UUID(as_uuid=True), sa.ForeignKey("transports.id"), nullable=True)
        ]
    ]
    location: orm.Mapped[typing.Annotated[list[int], orm.mapped_column(sa.ARRAY(sa.Integer), nullable=False)]]
    status: orm.Mapped[typing.Annotated[int, orm.mapped_column(sa.Integer, nullable=False)]]

    transport: orm.Mapped[typing.Optional["TransportsTable"]] = orm.relationship()


class OrdersTable(Base):
    __tablename__ = "orders"
    __allow_unmapped__ = True

    id: orm.Mapped[typing.Annotated[uuid.UUID, orm.mapped_column(postgresql.UUID(as_uuid=True), primary_key=True)]]
    location: orm.Mapped[typing.Annotated[list[int], orm.mapped_column(sa.ARRAY(sa.Integer), nullable=False)]]
    status: typing.Annotated[int, orm.mapped_column(sa.BigInteger, nullable=False)]
    courier_id: orm.Mapped[
        typing.Annotated[
            uuid.UUID, orm.mapped_column(postgresql.UUID(as_uuid=True), sa.ForeignKey("couriers.id"), nullable=True)
        ]
    ]
