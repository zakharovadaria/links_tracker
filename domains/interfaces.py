from abc import ABC, abstractmethod
from typing import List


class IDomainsDAO(ABC):
    @abstractmethod
    def add_domains(self, domains: List[str], current_time: float) -> bool:
        pass
