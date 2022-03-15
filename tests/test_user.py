
from fastapi import status
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

def test_login():
    data = {
        'firstname': 'Test user',
        'lastname': 'Test',
        'username': 'test_user',
        'password': '6g#-UKMrdZwF!Khq'
    }
    create_response = client.post('users/create', json=data)
    assert create_response.status_code == 200

    login_response = client.post('users/login', data={
        'username': data['username'],
        'password': data['password']
    })

    assert login_response.status_code == status.HTTP_200_OK
    token_data = login_response.json()
    assert 'access_token' in token_data 
