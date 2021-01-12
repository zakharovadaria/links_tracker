import json
from unittest import mock

from django.conf import settings
from django.test import TestCase, Client
from redis import Redis

from domains.daos import RedisDomainsDAO
from domains.use_cases import AddVisitedLinksUseCase


class RedisTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        self.redis = Redis.from_url(settings.TEST_REDIS_URL)
        self.redis.flushall()
        super().__init__(*args, **kwargs)


class DaoTestCase(RedisTestCase):
    def setUp(self) -> None:
        self.dao = RedisDomainsDAO(redis=self.redis)

    def test_add_domains(self):
        domains = ["first", "second", "third"]
        current_time = 1

        self.dao.add_domains(domains=domains, current_time=current_time)

        redis_data = self.redis.zrange("domains_set", 0, -1, withscores=True)
        domains, score = redis_data[0]
        domains = domains.decode("utf-8")
        list_domains = json.loads(domains)

        self.assertEqual(list_domains, ["first", "second", "third"])
        self.assertEqual(score, current_time)


class UseCaseTestCase(TestCase):
    def setUp(self) -> None:
        self.dao = mock.Mock()
        self.use_case = AddVisitedLinksUseCase(domains_dao=self.dao)

    def test_execute(self):
        links = [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor",
        ]
        current_time = 1
        self.dao.add_domains.return_value = True

        result = self.use_case.execute(links=links, current_time=current_time)

        self.assertEqual(result, True)
        self.dao.add_domains.assert_called_once_with(domains=[
            "ya.ru",
            "ya.ru",
            "funbox.ru",
            "stackoverflow.com",
        ], current_time=current_time)


class ViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_post(self):
        result = self.client.post("/visited_links", data=dict(
            links=[
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru",
                "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor",
            ],
        ), content_type="application/json")

        json_result = result.json()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json_result, {"status": "ok"})
