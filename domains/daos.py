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
