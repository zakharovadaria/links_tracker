from abc import ABC, abstractmethod
from typing import List


class IDomainsDAO(ABC):

    class BaseDomainException(Exception):
        pass

    class AddDataError(BaseDomainException):
        pass

    class GetDataError(BaseDomainException):
        pass

    @abstractmethod
    def add_domains(self, domains: List[str], current_time: float) -> None:
        pass

    @abstractmethod
    def get_domains(self, from_timestamp: int, to_timestamp: int) -> List[str]:
        pass
