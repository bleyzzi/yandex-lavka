import pytest
from tests.examples import AddCorrectRequestOrder, AddIncorrectRequestOrder
from tests.conftest import client


@pytest.mark.parametrize('data', AddCorrectRequestOrder.all_requests)
def test_add_new_order(data):
    response = client.post('/orders', json=data)
    assert response.status_code == 200


@pytest.mark.parametrize('data', AddIncorrectRequestOrder.all_requests_400)
def test_add_new_order_incorrect(data):
    response = client.post('/orders', json=data)
    assert response.status_code == 422


