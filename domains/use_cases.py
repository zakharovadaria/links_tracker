from typing import List, Set
from urllib.parse import urlparse

from domains.interfaces import IDomainsDAO


class AddVisitedLinksUseCase:

    class AddVisitedLinksError(Exception):
        pass

    def __init__(self, domains_dao: IDomainsDAO):
        self.domains_dao = domains_dao

    def execute(self, links: List[str], current_time: float) -> None:
        domains = list()

        for link in links:
            str_link = str(link)
            parse_result = urlparse(str_link)
            domain = parse_result.netloc

            if not domain:
                domain = parse_result.path

            if domain not in domains:
                domains.append(domain)

        try:
            self.domains_dao.add_domains(domains=domains, current_time=current_time)
        except self.domains_dao.AddDataError:
            raise self.AddVisitedLinksError


class GetUniqueVisitedDomainsUseCase:

    class GetVisitedDomainsError(Exception):
        pass

    def __init__(self, domains_dao: IDomainsDAO):
        self.domains_dao = domains_dao

    def execute(self, from_timestamp: int, to_timestamp: int) -> Set[str]:
        try:
            domains = self.domains_dao.get_domains(from_timestamp=to_timestamp, to_timestamp=from_timestamp)
            return set(domains)
        except self.domains_dao.GetDataError:
            raise self.GetVisitedDomainsError
