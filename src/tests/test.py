from http import HTTPStatus

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_get_db_status():
    response = client.get('api/v1/ping')
    assert response.status_code == HTTPStatus.OK
