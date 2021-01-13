from abc import ABC, abstractmethod
from typing import List


class IDomainsDAO(ABC):
    @abstractmethod
    def add_domains(self, domains: List[str], current_time: float) -> bool:
        pass

    @abstractmethod
    def get_domains(self, from_timestamp: int, to_timestamp: int) -> List[str]:
        pass
