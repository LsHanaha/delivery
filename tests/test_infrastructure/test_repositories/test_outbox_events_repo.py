import datetime

import faker
from that_depends import Provide, inject

from delivery import ioc
from delivery.core.application.models.outbox import OutboxEventModel
from delivery.infrastracture.adapters.postgres.repositories.outbox_repo import OutboxEventsRepository


FAKER_OBJ = faker.Faker()


@inject
async def test_add_outbox_event(
    outbox_repo: OutboxEventsRepository = Provide[ioc.IOCContainer.outbox_events_repo],
) -> None:
    created_event = await outbox_repo.add_event(
        OutboxEventModel(
            event={"azaza": "lalka"},
            topic="qweasd",
        ),
    )
    assert created_event
    assert created_event.id
    assert created_event.created_at


@inject
async def test_fetch_new_outbox_events(
    outbox_repo: OutboxEventsRepository = Provide[ioc.IOCContainer.outbox_events_repo],
) -> None:
    amount = 5
    for _ in range(amount):
        await outbox_repo.add_event(
            OutboxEventModel(
                event={"azaza": "lalka"},
                topic="qweasd",
            ),
        )
        await outbox_repo.add_event(
            OutboxEventModel(event={"azaza": "lalka"}, topic="qweasd", sent_at=datetime.datetime.now(tz=datetime.UTC)),
        )

    events = await outbox_repo.collect_all_new_events()
    assert events
    assert len(events) == amount


@inject
async def test_update_outbox_event(
    outbox_repo: OutboxEventsRepository = Provide[ioc.IOCContainer.outbox_events_repo],
) -> None:
    event = OutboxEventModel(
        event={"azaza": "lalka"},
        topic="qweasd",
    )
    created_event = await outbox_repo.add_event(event)
    assert created_event

    created_event.mark_as_sent()
    res = await outbox_repo.update_single_event(created_event)
    assert res
    assert res.sent_at
