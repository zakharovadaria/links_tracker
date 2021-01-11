from django.urls import path

from domains.daos import RedisDomainsDAO
from domains.use_cases import AddVisitedLinksUseCase
from domains.views import DomainsView

domains_dao = RedisDomainsDAO()
add_visited_links_use_case = AddVisitedLinksUseCase(domains_dao=domains_dao)

urlpatterns = [
    path('visited_links', DomainsView.as_view(
        add_visited_links_use_case=add_visited_links_use_case,
    )),
]
