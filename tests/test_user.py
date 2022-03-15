
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_create_user():
    data = {
        'firstname': 'Test user',
        'lastname': 'Test',
        'username': 'test_user',
        'password': '6g#-UKMrdZwF!Khq'
    }
    response = client.post('users/create', json=data)
    assert response.status_code == 200