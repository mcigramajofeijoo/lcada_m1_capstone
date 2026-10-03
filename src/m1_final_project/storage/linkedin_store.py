import os

from redis.asyncio import Redis


# This is populated with LINKEDIN_GET_MY_INFO tool!
class LinkedinStore:
    def __init__(self):
        self._redis = Redis.from_url(os.environ["REDIS_DB_URL"])
        self._key_prefix = "lcada:m1_fp:users:"

    def _get_key(self, user_id: str) -> str:
        return f"{self._key_prefix}:{user_id}:linkedin"

    async def set(self, user_id: str, urn: str):
        await self._redis.hset(name=self._get_key(user_id), mapping={"urn": urn})

    async def get(self, user_id):
        data = await self._redis.hgetall(name=self._get_key(user_id))

        if not data:
            return None

        return {k.decode(): v.decode() for k, v in data.items()}


linkedin_store = LinkedinStore()
