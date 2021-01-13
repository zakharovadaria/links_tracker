from unittest import TestCase

from django.conf import settings
from redis import Redis


class RedisTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        self.redis = Redis.from_url(settings.REDIS_URL)
        self.redis.flushall()
        super().__init__(*args, **kwargs)
        self.addCleanup(self.redis.flushall)
