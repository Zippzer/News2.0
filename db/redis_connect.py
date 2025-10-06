import redis
from service import token_env


r = redis.StrictRedis(
    host=token_env.REDIS_HOST,
    port=token_env.REDIS_PORT,
    password=token_env.REDIS_PASSWORD,
    charset="utf-8",
    decode_responses=True
)