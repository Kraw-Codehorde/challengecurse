import pytest
from django.core.management import call_command

"""
Fixtures for creating groups for the users before the tests are run.
"""

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('create_groups')

@pytest.fixture
def create_groups(db):
    call_command('create_groups')
