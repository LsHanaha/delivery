import typing
import uuid

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects import postgresql

from delivery.core.domain.model.courier_aggregate.courier_status import CourierStatusEnum
from delivery.core.domain.model.order_aggregate.order_status import OrderStatusEnum
from delivery.core.domain.shared.models import Location


METADATA: typing.Final = sa.MetaData()
Base = orm.declarative_base(metadata=METADATA)


class TransportsTable(Base):
    __tablename__ = "transports"

    id: orm.Mapped[typing.Annotated[uuid.UUID, orm.mapped_column(postgresql.UUID(as_uuid=True), primary_key=True)]]
    name: orm.Mapped[typing.Annotated[str, orm.mapped_column(sa.String, nullable=False)]]
    speed: orm.Mapped[typing.Annotated[int, orm.mapped_column(sa.Integer, nullable=False)]]

    courier: orm.Mapped[typing.Optional["CouriersTable"]] = orm.relationship(
        "CouriersTable", back_populates="transport"
    )


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
    coord_x: orm.Mapped[typing.Annotated[int, orm.mapped_column(sa.SmallInteger, nullable=False)]]
    coord_y: orm.Mapped[typing.Annotated[int, orm.mapped_column(sa.SmallInteger, nullable=False)]]

    location: orm.Mapped[Location] = orm.composite("coord_x", "coord_y")
    status: orm.Mapped[
        typing.Annotated[
            CourierStatusEnum, orm.mapped_column(sa.Enum(CourierStatusEnum, name="courier_status"), nullable=False)
        ]
    ]

    transport: orm.Mapped[typing.Optional["TransportsTable"]] = orm.relationship(
        "TransportsTable", back_populates="courier"
    )


class OrdersTable(Base):
    __tablename__ = "orders"
    __allow_unmapped__ = True

    id: orm.Mapped[typing.Annotated[uuid.UUID, orm.mapped_column(postgresql.UUID(as_uuid=True), primary_key=True)]]
    coord_x: orm.Mapped[typing.Annotated[int, orm.mapped_column(sa.SmallInteger, nullable=False)]]
    coord_y: orm.Mapped[typing.Annotated[int, orm.mapped_column(sa.SmallInteger, nullable=False)]]

    location: orm.Mapped[Location] = orm.composite("coord_x", "coord_y")
    status: orm.Mapped[
        typing.Annotated[
            CourierStatusEnum, orm.mapped_column(sa.Enum(OrderStatusEnum, name="order_status"), nullable=False)
        ]
    ]
    courier_id: orm.Mapped[
        typing.Annotated[
            uuid.UUID, orm.mapped_column(postgresql.UUID(as_uuid=True), sa.ForeignKey("couriers.id"), nullable=True)
        ]
    ]
