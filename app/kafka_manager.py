import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from app.config import settings


class KafkaManager:
    def __init__(self):
        self.producer = None
        self.consumer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_event(self, data: dict):
        await self.producer.send_and_wait(settings.KAFKA_TOPIC, data)

    async def start_consumer(self):
        consumer = AIOKafkaConsumer(
            settings.KAFKA_TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            group_id="test_group",
        )
        await consumer.start()
        try:
            async for msg in consumer:
                print("kafka_received:", msg.value)
        finally:
            await consumer.stop()


kafka_manager = KafkaManager()
