from arq.connections import RedisSettings

from ..config import settings
from .functions import sample_background_task, shutdown, startup


class WorkerSettings:
    functions = [
        sample_background_task,
    ]
    redis_settings = RedisSettings(
        host=settings.redis_queue.REDIS_HOST,
        port=settings.redis_queue.REDIS_PORT,
    )
    on_startup = startup
    on_shutdown = shutdown
    handle_signals = False
