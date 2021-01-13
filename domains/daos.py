import json
from typing import List

from redis import Redis, ResponseError

from domains.interfaces import IDomainsDAO


class RedisDomainsDAO(IDomainsDAO):

    def __init__(self, redis: Redis):
        self._redis = redis
        self.set_name = "domains_set"

    def add_domains(self, domains: List[str], current_time: float):
        domains_list_str = json.dumps(domains)

        try:
            self._redis.zadd(self.set_name, {domains_list_str: current_time})
        except ResponseError:
            raise self.AddDataError

    def get_domains(self, from_timestamp: int, to_timestamp: int) -> List[str]:
        try:
            result: List[bytes] = self._redis.zrangebyscore(self.set_name, from_timestamp, to_timestamp)
        except ResponseError:
            raise self.GetDataError

        domains_list = []

        for row in result:
            row_domains_list = json.loads(row.decode("utf-8"))
            domains_list.extend(row_domains_list)

        return domains_list
