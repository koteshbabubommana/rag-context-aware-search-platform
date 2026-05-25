import time


class CacheService:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        item = self.cache.get(key)

        if not item:
            return None

        value, expires_at = item

        if time.time() > expires_at:
            del self.cache[key]
            return None

        return value

    def set(self, key, value, ttl_seconds=300):
        expires_at = time.time() + ttl_seconds
        self.cache[key] = (value, expires_at)