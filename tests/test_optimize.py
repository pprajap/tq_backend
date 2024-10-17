# tests/test_optimize.py

import pytest
import json
import sys
import os

# Add the directory containing app.py to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_optimize(client):
    # Define the request payload
    payload = {
        "dimensions": 10,
        "lowerBound": -5.0,
        "upperBound": 5.0,
        "gridSizeFactorP": 2,
        "gridSizeFactorQ": 10,
        "evals": 1000,
        "funcName": "Simple",
        "isFunc": True,
        "isVect": True,
        "withCache": False,
        "withLog": True,
        "withOpt": False,
        "forceRecal": False
    }

    # Send a POST request to the /optimize endpoint
    response = client.post('/optimize', data=json.dumps(payload), content_type='application/json')

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response data
    response_data = response.get_json()
    assert "minimum_value" in response_data
    assert isinstance(response_data["minimum_value"], str)  # Assuming tto.info() returns a string

    # Print the response data for debugging
    print(response_data)

if __name__ == '__main__':
    pytest.main()