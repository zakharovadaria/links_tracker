import json
import time
from json.decoder import JSONDecodeError

from django.http import HttpRequest, JsonResponse
from django.views import View

from domains.use_cases import AddVisitedLinksUseCase, GetUniqueVisitedDomainsUseCase


class SuccessJsonResponse(JsonResponse):
    def __init__(self, data: dict = None, *args, **kwargs):
        if not data:
            data = {}
        data["status"] = "ok"
        super().__init__(*args, **kwargs, data=data)


class FailureJsonResponse(JsonResponse):
    def __init__(self, message: str, *args, **kwargs):
        json_response = {"status": "fail", "message": message}
        super().__init__(*args, **kwargs, data=json_response)


class VisitedLinksView(View):
    add_visited_links_use_case: AddVisitedLinksUseCase = None

    def post(self, request: HttpRequest) -> JsonResponse:
        current_time = int(time.time())

        try:
            visited_links = json.loads(request.body)
        except JSONDecodeError:
            return FailureJsonResponse(message="Body is not valid JSON")

        links = visited_links.get("links", [])

        if not isinstance(links, list):
            return FailureJsonResponse(message="Links should be array")

        if not links:
            return SuccessJsonResponse()

        try:
            self.add_visited_links_use_case.execute(links=links, current_time=current_time)
        except self.add_visited_links_use_case.AddVisitedLinksError:
            return FailureJsonResponse(message="There is a problem with settings data. Contact developer")

        return SuccessJsonResponse()


class VisitedDomainsView(View):
    get_unique_visited_domains_use_case: GetUniqueVisitedDomainsUseCase = None

    def get(self, request: HttpRequest) -> JsonResponse:
        from_timestamp = request.GET.get("from", None)
        to_timestamp = request.GET.get("to", None)

        if not from_timestamp:
            return FailureJsonResponse(message="Param 'from' is required")
        if not to_timestamp:
            return FailureJsonResponse(message="Param 'to' is required")

        try:
            num_from_timestamp = int(from_timestamp)
        except ValueError:
            return FailureJsonResponse(message="Param 'from' should be valid int")

        try:
            num_to_timestamp = int(to_timestamp)
        except ValueError:
            return FailureJsonResponse(message="Param 'to' should be valid int")

        try:
            result = self.get_unique_visited_domains_use_case.execute(
                from_timestamp=num_from_timestamp,
                to_timestamp=num_to_timestamp,
            )
        except self.get_unique_visited_domains_use_case.GetVisitedDomainsError:
            return FailureJsonResponse(message="There is a problem with getting data. Contact developer")

        return SuccessJsonResponse(data={"domains": list(result)})
