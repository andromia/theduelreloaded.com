import os
import tempfile

import pytest

from app import create_app
from app.utils import url_for
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    return app

def test_app(client):
    assert client.get(url_for('main.index')).status_code == 200

def test_new_user():
    user = User(username='owner', email='owner@email.com')
    user.set_password('test')
    assert user.email == 'owner@email.com'
    assert user.check_password('test')
    assert user.is_authenticated