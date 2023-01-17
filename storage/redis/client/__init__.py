import redis
from django.conf import settings

redis_pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)
redis_conn = redis.Redis(connection_pool=redis_pool)
