from typing import List, Optional
from urllib.parse import urlparse

from domains.interfaces import IDomainsDAO


class AddVisitedLinksUseCase:
    def __init__(self, domains_dao: IDomainsDAO):
        self.domains_dao = domains_dao

    def execute(self, links: List[str], current_time: float) -> bool:
        domains = list()

        for link in links:
            str_link = str(link)
            parse_result = urlparse(str_link)
            domain = parse_result.netloc

            if not domain:
                domain = parse_result.path

            domains.append(domain)

        return self.domains_dao.add_unique_domains(domains=domains, current_time=current_time)


class GetVisitedDomainsUseCase:
    class FromTimestampDoesNotExist(Exception):
        pass

    class ToTimestampDoesNotExit(Exception):
        pass

    class FromTimestampNotNumber(Exception):
        pass

    class ToTimestampNotNumber(Exception):
        pass

    def __init__(self, domains_dao: IDomainsDAO):
        self.domains_dao = domains_dao

    def execute(self, from_timestamp: Optional[str], to_timestamp: Optional[str]):
        if not from_timestamp:
            raise self.FromTimestampDoesNotExist()
        if not to_timestamp:
            raise self.ToTimestampDoesNotExit()

        try:
            num_from_timestamp = int(from_timestamp)
        except ValueError:
            raise self.FromTimestampNotNumber()

        try:
            num_to_timestamp = int(to_timestamp)
        except ValueError:
            raise self.ToTimestampNotNumber()

        return self.domains_dao.get_unique_domains(from_timestamp=num_from_timestamp, to_timestamp=num_to_timestamp)
