from django.conf import settings
from django.urls import path
from redis import Redis

from domains.daos import RedisDomainsDAO
from domains.use_cases import AddVisitedLinksUseCase, GetVisitedDomainsUseCase
from domains.views import VisitedLinksView, VisitedDomainsView

redis = Redis.from_url(settings.REDIS_URL)
domains_dao = RedisDomainsDAO(redis=redis)
add_visited_links_use_case = AddVisitedLinksUseCase(domains_dao=domains_dao)
get_visited_domains_use_case = GetVisitedDomainsUseCase(domains_dao=domains_dao)

urlpatterns = [
    path('visited_links', VisitedLinksView.as_view(
        add_visited_links_use_case=add_visited_links_use_case,
    )),
    path('visited_domains', VisitedDomainsView.as_view(
        get_visited_domains_use_case=get_visited_domains_use_case,
    )),
]
