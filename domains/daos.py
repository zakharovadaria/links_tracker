from typing import List

from domains.interfaces import IDomainsDAO


class RedisDomainsDAO(IDomainsDAO):
    def add_links(self, links: List[str]):
        pass
