from fastapi import FastAPI
from conf.app import AppSettings
from fastapi.logger import logger
from typing import Callable
import aioredis


async def connect_to_redis(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to Redis")
    app.state.redis = await aioredis.from_url(settings.redis_dsn,
                                            decode_responses=True,
                                            encoding="utf8")

    logger.info("Connection established")


def create_start_app_handler(app: FastAPI, settings: AppSettings)-> Callable:  # type: ignore
    async def start_app() -> None:
        await connect_to_redis(app, settings)
    return start_app


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to redis")
    await app.state.redis.close()
    logger.info("Connection closed")


def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def stop_app() -> None:
        await close_db_connection(app)
    return stop_app
