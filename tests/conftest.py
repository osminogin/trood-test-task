import pytest
import tempfile

from api.models import User, Upload


# @pytest.fixture(scope='session', autouse=True)
# def initial_data(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         management.call_command('loaddata', 'initial_data.json')


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope='function')
def example_upload():
    yield Upload.objects.create(
        file_name='example.csv',
        file_size=666,
        state=Upload.ACTIVE_STATE
    )


@pytest.fixture(scope='function')
def example_user():
    yield User.objects.create(
        first_name='Test',
        last_name='User',
        position='testuser',
        birth_date='1990-01-01'
    )


@pytest.fixture
def clients_csv():
    """ Тестовая база клиентов в CSV. """
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=True, mode='r+') as temp_csv:
        temp_csv.write('aaa,bbb,1990-01-01,ccc\n')
        temp_csv.write('ddd,eee,1990-02-02,fff\n')
        temp_csv.write('ggg,bbb,1990-03-03,ccc\n')
        temp_csv.write('eee,hhh,1990-04-04,xxx\n')
        temp_csv.seek(0)
        yield temp_csv
