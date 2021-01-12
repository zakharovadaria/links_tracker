from typing import List
from urllib.parse import urlparse

from domains.interfaces import IDomainsDAO


class AddVisitedLinksUseCase:
    def __init__(self, domains_dao: IDomainsDAO):
        self.domains_dao = domains_dao

    def execute(self, links: List[str], current_time: float) -> bool:
        domains = []

        for link in links:
            str_link = str(link)
            parse_result = urlparse(str_link)
            domain = parse_result.netloc

            if not domain:
                domain = parse_result.path

            domains.append(domain)

        return self.domains_dao.add_domains(domains=domains, current_time=current_time)
