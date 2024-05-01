import redis
from src.config import EnvConfig
from typing import Union

class Cache:
    def __init__(self, config: EnvConfig):
        self.client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
    
    def set(self, key: str, value: str):
        expiration_time_seconds = 300 # 5 mins
        self.client.set(key, value)
        self.client.expire(key, expiration_time_seconds)
    
    def get(self, key: str) -> Union[str, None]:
        value = self.client.get(key)
        if value is not None:
            res = value.decode('utf-8')
            return res
        return None


