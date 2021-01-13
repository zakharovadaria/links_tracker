from unittest import TestCase, mock

from domains.interfaces import IDomainsDAO
from domains.use_cases import AddVisitedLinksUseCase, GetUniqueVisitedDomainsUseCase


class VisitedLinksUseCaseTestCase(TestCase):

    def setUp(self) -> None:
        self.dao = mock.Mock()
        self.dao.AddDataError = IDomainsDAO.AddDataError
        self.use_case = AddVisitedLinksUseCase(domains_dao=self.dao)

    def test_execute_without_exception(self):
        links = [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor",
        ]
        current_time = 1

        self.use_case.execute(links=links, current_time=current_time)

        self.dao.add_domains.assert_called_once_with(domains=[
            "ya.ru",
            "funbox.ru",
            "stackoverflow.com",
        ], current_time=current_time)

    def test_execute_with_exception(self):
        links = [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor",
        ]
        current_time = 1
        self.dao.add_domains.side_effect = IDomainsDAO.AddDataError

        with self.assertRaises(self.use_case.AddVisitedLinksError):
            self.use_case.execute(links=links, current_time=current_time)

            self.dao.add_domains.assert_called_once_with(domains=[
                "ya.ru",
                "funbox.ru",
                "stackoverflow.com",
            ], current_time=current_time)


class VisitedDomainsTestCase(TestCase):

    def setUp(self) -> None:
        self.dao = mock.Mock()
        self.dao.GetDataError = IDomainsDAO.GetDataError
        self.use_case = GetUniqueVisitedDomainsUseCase(domains_dao=self.dao)

    def test_execute_without_exception(self):
        from_timestamp = 0
        to_timestamp = 1
        self.dao.get_domains.return_value = ["1", "1", "2"]

        result = self.use_case.execute(from_timestamp=from_timestamp, to_timestamp=to_timestamp)

        self.assertEqual(result, set(["1", "2"]))
        self.assertCountEqual(result, ["1", "2"])
        self.dao.get_domains.assert_called_once_with(from_timestamp=to_timestamp, to_timestamp=from_timestamp)

    def test_execute_with_exception(self):
        from_timestamp = 0
        to_timestamp = 1
        self.dao.get_domains.side_effect = IDomainsDAO.GetDataError

        with self.assertRaises(self.use_case.GetVisitedDomainsError):
            self.use_case.execute(from_timestamp=from_timestamp, to_timestamp=to_timestamp)

            self.dao.get_domains.assert_called_once_with(from_timestamp=to_timestamp, to_timestamp=from_timestamp)
