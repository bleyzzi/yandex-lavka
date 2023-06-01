import pytest
from tests.examples import AddCorrectRequestCourier, AddIncorrectRequestCourier
from tests.conftest import client


@pytest.mark.parametrize('data', AddCorrectRequestCourier.all_requests)
def test_add_new_courier_correct(data):
    response = client.post('/couriers', json=data)
    assert response.status_code == 200


@pytest.mark.parametrize('data', AddIncorrectRequestCourier.all_requests_400)
def test_add_new_courier_incorrect(data):
    response = client.post('/couriers', json=data)
    assert response.status_code == 400


@pytest.mark.parametrize('data', AddIncorrectRequestCourier.all_requests_422)
def test_add_new_courier_incorrect(data):
    response = client.post('/couriers', json=data)
    assert response.status_code == 422


@pytest.mark.parametrize('limit, offset', [(1, 0), (1, 1), (10, 0), (10, 10)])
def test_get_courier_info(limit, offset):
    client.post('/couriers', json={
        "couriers": [{"courier_type": "AUTO", "regions": [1], "working_hours": ["12:00-14:00"]}
                     ]}
                )
    params = {
        'limit': limit,
        'offset': offset
    }
    response = client.get('/couriers', params=params)
    assert response.status_code == 200


def test_get_courier_info_by_correct_id():
    client.post('/couriers', json={
        "couriers": [{"courier_type": "AUTO", "regions": [1], "working_hours": ["12:00-14:00"]}
                     ]}
                )
    response = client.get('/couriers/1')
    assert response.status_code == 200


def test_get_courier_info_by_incorrect_id():
    client.post('/couriers', json={
        "couriers": [{"courier_type": "AUTO", "regions": [1], "working_hours": ["12:00-14:00"]}
                     ]}
                )
    response = client.get('/couriers/99999')
    assert response.status_code == 404
