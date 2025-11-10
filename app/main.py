import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import router
from app.kafka_manager import kafka_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_manager.start()
    print("kafka producer started")
    consumer_task = asyncio.create_task(kafka_manager.start_consumer())
    print("kafka consumer started")
    yield
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass
    await kafka_manager.stop()
    print("kafka producer stopped!!!!!")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
