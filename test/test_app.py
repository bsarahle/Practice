# tests/test_app.py
import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

def test_get_items(client):
    response = client.get('/items')
    assert response.status_code == 200
    assert b'[]' in response.data  # Assuming the database is empty initially
