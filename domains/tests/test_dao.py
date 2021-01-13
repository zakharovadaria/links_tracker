import json

from domains.daos import RedisDomainsDAO
from domains.tests import RedisTestCase


class DaoTestCase(RedisTestCase):
    def setUp(self) -> None:
        self.dao = RedisDomainsDAO(redis=self.redis)

    def test_add_domains(self):
        domains = ["first", "second", "third"]
        current_time = 1

        self.dao.add_domains(domains=domains, current_time=current_time)

        redis_data = self.redis.zrange("domains_set", 0, -1, withscores=True)
        domains, score = redis_data[0]
        domains = domains.decode("utf-8")
        list_domains = json.loads(domains)

        self.assertEqual(list_domains, ["first", "second", "third"])
        self.assertEqual(score, current_time)

    def test_get_domains(self):
        self.redis.zadd("domains_set", {json.dumps(["first", "second"]): 1, json.dumps(["third"]): 20})

        from_timestamp = 0
        to_timestamp = 10

        result = self.dao.get_domains(from_timestamp=from_timestamp, to_timestamp=to_timestamp)

        self.assertEqual(result, ["first", "second"])
