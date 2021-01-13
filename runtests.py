#!/usr/bin/env python
import os
import sys

import django

from links_tracker.test_runner import NoDBTestRunner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'links_tracker.test_settings'
    django.setup()
    test_runner = NoDBTestRunner()
    failures = test_runner.run_tests(["domains"])
    sys.exit(bool(failures))
