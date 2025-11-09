from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import router
from app.kafka_manager import kafka_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_manager.start()
    print("kafka producer started...")
    yield
    await kafka_manager.stop()
    print("kafka producer stopped...")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
