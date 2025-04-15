from faststream import FastStream
from faststream.kafka import KafkaBroker

from delivery.settings import settings


broker = KafkaBroker(settings.kafka_dsn)
app = FastStream(broker=broker)
