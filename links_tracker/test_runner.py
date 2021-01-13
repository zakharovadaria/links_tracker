from django.test.runner import DiscoverRunner


class NoDBTestRunner(DiscoverRunner):
    def setup_databases(self, *args, **kwargs):
        pass

    def teardown_databases(self, *args, **kwargs):
        pass
