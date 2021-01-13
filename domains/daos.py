import json
from typing import List

from redis import Redis, ResponseError

from domains.interfaces import IDomainsDAO


class RedisDomainsDAO(IDomainsDAO):
    def __init__(self, redis: Redis):
        self._redis = redis

    def add_domains(self, domains: List[str], current_time: float) -> bool:
        if not domains:
            return False

        domains_list_str = json.dumps(domains)

        try:
            self._redis.zadd("domains_set", {domains_list_str: current_time})
        except ResponseError as e:
            return False

        return True

    def get_domains(self, from_timestamp: int, to_timestamp: int) -> List[str]:
        result: List[bytes] = self._redis.zrangebyscore("domains_set", to_timestamp, from_timestamp)
        domains_set = set()

        for row in result:
            domains_list = json.loads(row.decode("utf-8"))
            domains_set = domains_set.union(set(domains_list))

        return list(domains_set)
