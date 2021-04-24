#!/usr/bin/env python3

import pytest
from app import check_url_status, name_reverser, name
from datetime import datetime, timedelta

@pytest.mark.skip(reason='misunderstood the API')
def test_check_url_status():
    assert check_url_status('http://mail.de') == 200

#@pytest.mark.skipif(name == 'demo', reason='Dont test if name is demo')
@pytest.mark.xfail()
def test_name_reverser():
    assert name_reverser("demo") == "omed1"

def test_name_reverser2():
    assert name_reverser("demo") == "omed"

@pytest.mark.check_url
@pytest.mark.important
@pytest.mark.login
@pytest.mark.skip("sometimes hangs and causes delay of tests")
def test_check_url_status2():
    assert check_url_status('http://www.az') == 200

@pytest.mark.parametrize('a, b, s', [(3, 4, 7), (5, 6, 11), (7, 11, 18)] )
def test_summ(a, b, s):
    #assert summ(3, 5) == 8
    #assert equivalent(t_from_db, task)
    assert a + b == s

testdata = [
    (datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1)),
    (datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1)),
]

@pytest.mark.parametrize("a,b,expected", testdata)
def test_timedistance_v0(a, b, expected):
    diff = a - b
    assert diff == expected


@pytest.fixture()
def some_data():
    return 42

def test_some_data(some_data):
    assert some_data == 42

@pytest.mark.usefixtures()
def test_get_url_status_code(get_url_status_code):
    assert get_url_status_code == 200

