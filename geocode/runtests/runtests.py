#!/usr/bin/env python

import os
import sys

# fix sys path so we don't need to setup PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
os.environ['DJANGO_SETTINGS_MODULE'] = 'geocode.runtests.settings'


import django
from django.conf import settings
from django.test.utils import get_runner


def main():
    try:
        django.setup()
    except AttributeError:
        pass
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['geocode.tests'])
    sys.exit(failures)


if __name__ == '__main__':
    main()
