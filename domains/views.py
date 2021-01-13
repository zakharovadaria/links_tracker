import json
import time

from django.http import HttpRequest, JsonResponse
from django.views import View

from domains.use_cases import AddVisitedLinksUseCase, GetVisitedDomainsUseCase


class VisitedLinksView(View):
    add_visited_links_use_case: AddVisitedLinksUseCase = None

    def post(self, request: HttpRequest) -> JsonResponse:
        current_time = time.time()

        visited_links = json.loads(request.body)
        links = visited_links.get("links", [])

        result = self.add_visited_links_use_case.execute(links=links, current_time=current_time)

        if not result:
            return JsonResponse({"status": "fail"})

        return JsonResponse({"status": "ok"})


class VisitedDomainsView(View):
    get_visited_domains_use_case: GetVisitedDomainsUseCase = None

    def get(self, request: HttpRequest) -> JsonResponse:
        from_timestamp = request.GET.get("from", None)
        to_timestamp = request.GET.get("to", None)

        result = self.get_visited_domains_use_case.execute(from_timestamp=from_timestamp, to_timestamp=to_timestamp)
        return JsonResponse({"status": "ok", "domains": result})
