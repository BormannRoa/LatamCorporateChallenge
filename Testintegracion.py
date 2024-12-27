import requests

def test_api_response():
    response = requests.get('https://your-function-app-url/api/your-endpoint')
    assert response.status_code == 200
    data = response.json()
    assert 'expected_key' in data
    assert data['expected_key'] == 'expected_value'
