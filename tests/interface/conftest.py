""" Interface Testing is performed to evaluate whether service's internal
    components act as expected.
    These tests (unlike unit tests) should use real entrypoints to trigger
    service's functionality.
    Interface tests will often use real dependencies when appropriate.
    When to use mocked vs real dependencies:
    Use mock for dependencies that deal with external services which are not a
    part of service's bounded context.
    User real dependencies for testing interaction with internal systems that
    you have a full control of like databases and file systems.
    Dependencies themselves should all have their own
    set of unit and interface tests.
"""

import pytest

from books.services import BooksService

@pytest.fixture
def config():
    return {
        "DB_URIS": {"books_service:Base": 'postgresql://postgres:password@localhost:5433/books_DB'},
        "AMQP_URI": "amqp://guest:guest@127.0.0.1:5672",
        "serializer": "pickle",
    }


@pytest.fixture
def create_svc(container_factory, config):
    service_container = container_factory(BooksService, config)
    service_container.start()
    yield service_container
    service_container.stop()
