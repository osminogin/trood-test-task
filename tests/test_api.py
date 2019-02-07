import uuid
from time import sleep

import pytest
import requests
from django.urls import reverse
from rest_framework import status

from api.models import User


def test_api_import_create(clients_csv, client):
    """ Тестирование импорта. """
    assert not User.objects.count()
    result = client.post(
        reverse('v1:import-list'),
        {'file': clients_csv.file}
    )
    assert result.status_code == status.HTTP_201_CREATED
    assert not result.data
    assert User.objects.count() > 0


def test_api_import_create(clients_csv, client):
    """ Тестирование импорта. """
    assert not User.objects.count()
    result = client.post(
        reverse('v1:import-list'),
        {'file': clients_csv.file}
    )
    assert result.status_code == status.HTTP_201_CREATED
    assert not result.data
    assert User.objects.count() > 0


def test_api_empty_activity_list(client):
    """ Пустой список активных загрузок. """
    result = client.get(reverse('v1:activity-list'))
    assert result.status_code == status.HTTP_200_OK
    assert not result.data


def test_api_activity_list(client, example_upload):
    """ Список активных загрузок. """
    result = client.get(reverse('v1:activity-list'))
    assert result.status_code == status.HTTP_200_OK
    assert result.data
    assert len(result.data) == 1
    data = result.data.pop()
    assert 'file_name' in data
    assert 'started' in data


def test_api_clients_search_all(client, example_user):
    """ Список всех пользователей (фильтр не используется). """
    result = client.get(reverse('v1:search-list'))
    assert result.status_code == status.HTTP_200_OK, result.data
    assert len(result.data) == 1
    data = result.data.pop()
    assert 'first_name' in data
    assert 'last_name' in data
    assert 'birth_date' in data
    assert 'position' in data


def test_api_clients_search(client, example_user):
    """ Тестирование поиска по списку пользователей. """
    result = client.get(
        reverse('v1:search-list'),
        {'str': uuid.uuid4()}
    )
    assert result.status_code == status.HTTP_200_OK
    assert not result.data

    # Поиск по имени ИЛИ фамилии
    result = client.get(
        reverse('v1:search-list'),
        {'str': example_user.first_name}
    )
    assert result.status_code == status.HTTP_200_OK
    assert result.data
    assert len(result.data) == 1

    # Поиск по имени И фамилии
    result = client.get(
        reverse('v1:search-list'),
        {'str': f'{example_user.first_name} {example_user.last_name}'}
    )
    assert result.status_code == status.HTTP_200_OK
    assert result.data
    assert len(result.data) == 1

    # Другая фамилия - пустой список
    result = client.get(
        reverse('v1:search-list'),
        {'str': f'{example_user.first_name} {example_user.last_name}666'}
    )
    assert result.status_code == status.HTTP_200_OK
    assert not result.data


@pytest.mark.realtest
def test_chunked_file_upload(client):
    def gen():
        return
        yield b'hi'
        sleep(10)
        yield b'there'

    response = requests.post(
        'http://localhost:8000/v1/import/',
        files={'file': open('../README.md', 'r')}
    )
    assert response.status_code == status.HTTP_201_CREATED
