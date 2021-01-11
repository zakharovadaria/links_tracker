from typing import List

from domains.interfaces import IDomainsDAO


class AddVisitedLinksUseCase:
    def __init__(self, domains_dao: IDomainsDAO):
        self.domains_dao = domains_dao

    def execute(self, links: List[str]):
        return self.domains_dao.add_links(links=links)
