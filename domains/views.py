import json

from django.http import HttpRequest, JsonResponse
from django.views import View

from domains.use_cases import AddVisitedLinksUseCase


class DomainsView(View):
    add_visited_links_use_case: AddVisitedLinksUseCase = None

    def post(self, request: HttpRequest) -> JsonResponse:
        visited_links = json.loads(request.body)
        links = visited_links.get("links", [])
        self.add_visited_links_use_case.execute(links=links)

        return JsonResponse({"status": "ok"})
