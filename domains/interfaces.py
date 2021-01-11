from abc import ABC, abstractmethod
from typing import List


class IDomainsDAO(ABC):
    @abstractmethod
    def add_links(self, links: List[str]):
        pass
