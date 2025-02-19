from arq.connections import ArqRedis

from .redis_client import pool

# uncomment if you use another redis for queue
# pool: ArqRedis | None = None

pool = ArqRedis(pool)
