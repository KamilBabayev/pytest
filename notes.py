Tests


Unit test: 
A test that checks a small bit of code, like a function or a class, in isolation of the rest of the system.

Integration test:
A test that checks a larger bit of the code, maybe several classes, or a subsystem. Mostly it’s a label 
used for some test larger than a unit test, but smaller than a system test.

System test (end-to-end): 
A test that checks all of the system under test in an environment as close to the end-user environment as possible.

Functional test: 
A test that checks a single bit of functionality of a system. A test that checks how well we add or 
delete or update a task item in Tasks is a functional test.

Subcutaneous test: A test that doesn’t run against the final end-user interface, but against an interface 
just below the surface. Since most of the tests in this book test against the API layer—not the CLI—they 
qualify as subcutaneous tests.


~~~~~~~~~~~~~~~
Given no arguments, pytest looks at your current directory and all subdirectories for test files and 
runs the test code it finds. It looks for files starting with test_ or ending with _test

To get just our new task tests to run, you can give pytest all the filenames you want run, or the directory, 
or call pytest from the directory where our tests are

• Test files should be named test_<something>.py or <something>_test.py .
• Test methods and functions should be named test_<something> .
• Test classes should be named Test<Something> .

Configuration files could be pytest.ini , tox.ini , or setup.cfg.

~~~~~~~~~~~~~~~~~~
Here are the possible outcomes of a test function:
• PASSED (.): The test ran successfully.
• FAILED (F): The test did not run successfully (or XPASS + strict).
• SKIPPED (s): The test was skipped. You can tell pytest to skip a test by using either the @pytest.mark.skip() 
               or pytest.mark.skipif() decorators.
• xfail (x): The test was not supposed to pass, ran, and failed. You can tell pytest that a test is expected 
             to fail by using the @pytest.mark.xfail() decorator.
• XPASS (X): The test was not supposed to pass, ran, and passed.
• ERROR (E): An exception happened outside of the test function, in either a fixture


Running only one test
pytest -v tasks/test_four.py::test_asdict
pytest -v make_test.py::test_name_reverser

~~~~~~~~~~~~~~~~~~~~~~
pytest options
-v --verbose
pytest make_test.py --collect-only -shows you which tests will be run with the given options and configuration.

-m markexpr
Markers are one of the best ways to mark a subset of your test functions so that they can be run together. 
As an example, one way to run test_replace() and test_member_access() , even though they are in separate files, 
is to mark them:

@pytest.mark.run_these_please
def test_member_access():
...

then
pytest -v -m run_these_please            - run like this.

pytest -v  make_test.py -m login
pytest -v  make_test.py -m "important and login"

-x, –exitfirst  -  exit on fist failed test and dont run all tests if one failed.(which is default.)
–maxfail=num    - specify how many failures are okay with you.

--lf ,   -last-failed    - run  just the failing test
-ff,  --failed-first    - run failed test firstm  then others.
--quite, -q  - oposite of verbose


--durations:
The --durations=N option is incredibly helpful when you’re trying to speed up your test suite. It doesn’t 
change how your tests are run; it reports the slowest N number of tests/setups/teardowns after the tests run. 
If you pass in --durations=0 , it reports everything in order of slowest to fastest.

pytest   make_test.py   --durations=0 -vv       #  will show all calls and delays of them


Every test essentially has three phases: call, setup, and teardown. Setup and teardown are also called 
fixtures and are a chance for you to add code to get data or the software system under test into a
precondition state before the test runs, as well as clean up afterwards if necessary.


Pytest includes a few helpful builtin markers:  skip,  skipif, xfail
@pytest.mark.skip(reason='misunderstood the API')   -  we can skip test with this way


We can skip  if defined condition is true
@pytest.mark.skipif(tasks.__version__ < '0.2.0', reason='not supported until version 0.2.0')

Nice output
pytest make_test.py -v -rs

@pytest.mark.xfail()    -  expected to fail but passed.

To run specific test
pytest make_test.py::test_name_reverser -v -rs
pytest make_test.py::TestClass -v -rs
pytest make_test.py::TestClass::test_method -v -rs

Run tests which has specified name, keyword afer  -k option
pytest make_test.py -v -rs -k reverser


Parametrized tests
@pytest.mark.parametrize('a, b, s', [(3, 4, 7), (5, 6, 11), (7, 11, 18)] )
def test_summ(a, b, s):
    #assert summ(3, 5) == 8
    #assert equivalent(t_from_db, task)
    assert a + b == s


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fixtures:
Fixtures are functions that are run by pytest before (and sometimes after) the actual test functions. 
The code in the fixture can do whatever you want it to. You can use fixtures to get a data set for 
the tests to work on. You can use fixtures to get a system into a known state before running a test. 
Fixtures are also used to get data ready for multiple tests.

The @pytest.fixture() decorator is used to tell pytest that a function is a fixture. When you include 
the fixture name in the parameter list of a test function, pytest knows to run it before running the test. 
Fixtures can do work, and can also return data to the test function.

@pytest.fixture()
def some_data():
    """Return answer to ultimate question."""
    return 42

def test_some_data(some_data):
    """Use fixture return value in a test."""
    assert some_data == 42

The test test_some_data() has the name of the fixture, some_data , as a parameter. pytest will see this and 
look for a fixture with this name. Fixture functions often set up or retrieve some data that the test can work
with. Sometimes this data is considered a fixture. For example, the Django community often uses fixture to mean 
some initial data that gets loaded into a database at the start of an application.
  test fixtures refer to the mechanism pytest provides to allow the separation of “getting ready
for” and “cleaning up after” code from your test functions.
  You can put fixtures into individual test files, but to share fixtures among multiple test files, 
you need to use a conftest.py file somewhere centrally located for all of the tests.


import pytest
import tasks
from tasks import Task
@pytest.fixture()
def tasks_db(tmpdir):
    """Connect to db before tests, disconnect after."""
    # Setup : start db
    tasks.start_tasks_db(str(tmpdir), 'tiny')
    yield
    # this is where the testing happens
    # Teardown : stop db
    tasks.stop_tasks_db()

The value of tmpdir isn’t a string—it’s an object that represents a directory.
However, it implements __str__ , so we can use str() to get a string to pass to
start_tasks_db() . We’re still using 'tiny' for TinyDB, for now.
A fixture function runs before the tests that use it. However, if there is a yield
in the function, it stops there, passes control to the tests, and picks up on
the next line after the tests are done. Therefore, think of the code above the
yield as “setup” and the code after yield as “teardown.” The code after the yield ,
the “teardown,” is guaranteed to run regardless of what happens during the
tests.


Added this to conftest.py  file 
@pytest.fixture
def get_url_status_code():
    req = requests.get('https://facebook.com')
    return req.status_code

then used this fixture in make_test.py file
def test_get_url_status_code(get_url_status_code):
    assert get_url_status_code == 200


pytest  make_test.py -v -rs --setup-show    - Tracing Fixture Execution with –setup-show

Fixtures are a great place to store data to use for testing. You can return anything.

As example to fixture. for ex:  we should connect and get some data and then make tests on this data.
instead of writing DB connection and data retrieval part inside test function we write it in separate fixture
and also write separate test function which will take that data and make tests. So test function will not engage
with db connections and data retrieval which it should not do for best practise.

~~~~~~~~~~~~
Specifiying Fixture Scope

Fixtures include an optional parameter called scope , which controls how often a fixture gets set up and torn down.
The scope parameter to @pytest.fixture() can have the values of function , class , module , or session.
The default scope is function.
scope='function'
scope='class'
scope='module'
scope='session'


@pytest.fixture(scope='session')
def func_scope():
"""A function scope fixture."""



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Builtin fixtures
Reusing common fixtures is such a good idea that the pytest developers included some commonly needed fixtures with pytest.
The builtin fixtures that come prepackaged with pytest can help you do some pretty useful things in your tests easily 
and consistently. For example, in addition to handling temporary files, pytest includes builtin fixtures to access
command-line options, communicate between tests sessions, validate output streams, modify environmental variables, 
and interrogate warnings.
  The tmpdir and tmpdir_factory builtin fixtures are used to create a temporary file system directory before your test runs, 
and remove the directory when your test is finished.


With the pytestconfig builtin fixture, you can control how pytest runs through command-line arguments and options, 
configuration files, plugins, and the directory from which you launched pytest.

add this to conftest.py  file:
def pytest_addoption(parser):
    parser.addoption("--myopt", action="store_true",
                     help="some boolean option")
    parser.addoption("--foo", action="store", default="bar",
                     help="foo: bar or baz")
    parser.addoption("--host", action="store", help="provide host name")

Cache
However, sometimes passing information from one test session to the next can be quite useful. When we do want to pass 
information to future test sessions, we can do it with the cache builtin fixture. A great example of using the powers 
of cache for good is the builtin functionality of --last-failed and --failed-first .



pytest  --verbose --tb=no  simple_test.py       - run test
pytest  --verbose --tb=no --ff  simple_test.py  - will run failed test first
pytest  --verbose --tb=no --lf  simple_test.py  - will run only failed test

--cache-show    show cache contents, do not perform collection or tests
--cache-clear   remove all cache contents at start of test run.

~~~
monkeymatch
A “monkey patch” is a dynamic modification of a class or module during runtime.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Plugins
The pytest code base is structured with customization and extensions, and there are hooks available to allow 
modifications and improvements through plugins.

pytest plugins are installed with pip:    pip intall pytest-cov




~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Configuration
configuration files that affect pytest
pytest.ini :     This is the primary pytest configuration file that allows you to change default behavior. 
Since there are quite a few configuration changes you can make, a big chunk of this chapter is about the 
settings you can make in pytest.ini.

conftest.py : This is a local plugin to allow hook functions and fixtures for the directory where the 
conftest.py file exists and all subdirectories

__init__.py : When put into every test subdirectory, this file allows you to have identical test filenames 
in multiple test directories.

tox.ini : This file is similar to pytest.ini , but for tox. However, you can put your pytest configuration 
here instead of having both a tox.ini and a pytest.ini file, saving you one configuration file.

setup.cfg : This is a file that’s also in ini file format and affects the behavior of setup.py . It’s possible to 
add a couple of lines to setup.py to allow you to run python setup.py test and have it run all of your pytest tests.


Ex:   pytest.ini
addopts = -rsxX -v    - if we added this to pytest.ini this will be default pytest command options when we run pytest.

We can run pytest --help    command and se pytest ini-options from there also.

Requiring mimimum pytest version
[pytest]
minversion = 3.0

Stopping pytest  from looking in wrong places.
[pytest]
norecursedirs = .* venv src *.egg dist build


Specifying test directories
[pytest]
testpaths = tests


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Using pytest with Other Tools
pytest -v --lf -x --pdb

Coverage.py: Determining How Much Code Is Tested

