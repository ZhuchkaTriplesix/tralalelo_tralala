from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka import AIOKafkaProducer
import asyncio
import json

TOPIC_NAMES = ["crud-create", "crud-read", "crud-update", "crud-delete"]


async def get_kafka_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await producer.start()
    return producer


async def create_topics():
    admin_client = AIOKafkaAdminClient(bootstrap_servers="kafka:9092")
    await admin_client.start()
    try:
        existing = await admin_client.list_topics()
        new_topics = [
            NewTopic(name=topic, num_partitions=1, replication_factor=1)
            for topic in TOPIC_NAMES if topic not in existing
        ]
        if new_topics:
            await admin_client.create_topics(new_topics)
            print(f"Created topics: {[t.name for t in new_topics]}")
    finally:
        await admin_client.close()


async def send_kafka_message(topic: str, message: dict):
    producer = await get_kafka_producer()
    await producer.send_and_wait(topic, message)


async def close_kafka_producer():
    global producer
    if producer:
        await producer.stop()
        producer = None
