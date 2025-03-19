import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """
    Create a test client for the app.
    """
    return TestClient(app)
