import json

from django.test import Client

from domains.tests import RedisTestCase


class ViewsTestCase(RedisTestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_post_with_not_list_links(self):
        result = self.client.post("/visited_links", data={"links": "123"}, content_type="application/json")

        json_result = result.json()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json_result, {"status": "fail", "message": "Links should be array"})

    def test_post_with_empty_array(self):
        result = self.client.post("/visited_links", data={"links": []}, content_type="application/json")

        json_result = result.json()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json_result, {"status": "ok"})

    def test_post(self):
        result = self.client.post("/visited_links", data={"links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor",
        ]}, content_type="application/json")

        json_result = result.json()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json_result, {"status": "ok"})

    def test_get_without_from(self):
        result = self.client.get("/visited_domains?to=1545217638")

        json_result = result.json()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json_result, {"status": "fail", "message": "Param 'from' is required"})

    def test_get_without_to(self):
        result = self.client.get("/visited_domains?from=1545217638")

        json_result = result.json()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json_result, {"status": "fail", "message": "Param 'to' is required"})

    def test_get_from_not_number(self):
        result = self.client.get("/visited_domains?from=qwerty&to=2")

        json_result = result.json()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json_result, {"status": "fail", "message": "Param 'from' should be valid int"})

    def test_get_to_not_number(self):
        result = self.client.get("/visited_domains?from=1&to=qwerty")

        json_result = result.json()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json_result, {"status": "fail", "message": "Param 'to' should be valid int"})

    def test_get(self):
        self.redis.zadd("domains_set", {
            json.dumps([
                "ya.ru",
                "ya.ru",
                "funbox.ru",
                "stackoverflow.com",
            ]): 2,
            json.dumps([
                "ya.ru",
                "ya.ru",
                "stackoverflow.com",
            ]): 4,
        })

        result = self.client.get("/visited_domains?from=10&to=0")

        json_result = result.json()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json_result["status"], "ok")
        self.assertEqual(set(json_result["domains"]), {"ya.ru", "funbox.ru", "stackoverflow.com"})
        self.assertCountEqual(json_result["domains"], ["ya.ru", "funbox.ru", "stackoverflow.com"])
