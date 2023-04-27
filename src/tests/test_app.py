import pytest
from fastapi.testclient import TestClient


def test_ping(client: TestClient):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.json() == 'pong'


@pytest.mark.parametrize('username', ['user1', 'alisa'])
def test_hello_username(client: TestClient, username: str):
    response = client.post('/hello', json={'username': username})
    assert response.status_code == 200
    assert response.json() == f'Hello, {username}!'
