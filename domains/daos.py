import json
from typing import List

from redis import StrictRedis

from domains.interfaces import IDomainsDAO


class RedisDomainsDAO(IDomainsDAO):
    def __init__(self, redis_url: str):
        self._redis = StrictRedis.from_url(url=redis_url)

    def add_links(self, links: List[str], current_time: float) -> int:
        links_list_str = json.dumps(links)
        count_links = self._redis.zadd("domains_set", {links_list_str: current_time})

        return count_links
