# coding: utf-8
from __future__ import print_function

import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def setup_and_run_tests(test_labels=None):
    """Discover and run project tests. Returns number of failures."""
    test_labels = test_labels or ['fack.tests']

    # noinspection PyStringFormat
    os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'
    django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1)
    return test_runner.run_tests(test_labels)


def runtests(test_labels=None):
    """Run project tests and exit"""
    # Used as setup test_suite: must either exit or return a TestSuite
    failures = setup_and_run_tests(test_labels)
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests(test_labels=sys.argv[1:])
