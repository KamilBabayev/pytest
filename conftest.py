
import pytest
import requests

@pytest.fixture
def get_url_status_code():
    '''return status code from request '''
    req = requests.get('https://facebook.com')
    return req.status_code

def pytest_addoption(parser):
    parser.addoption("--myopt", action="store_true",
                     help="some boolean option")
    parser.addoption("--foo", action="store", default="bar",
                     help="foo: bar or baz")
    parser.addoption("--host", action="store", help="provide host name")

def pytest_report_header():
    """Thank tester for running tests."""
    return "Thanks for running the tests."

def pytest_report_teststatus(report):
    """Turn failures into opportunities."""
    if report.when == 'call' and report.failed:
        return (report.outcome, 'O', 'OPPORTUNITY for improvement')
