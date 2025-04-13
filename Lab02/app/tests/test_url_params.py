def test_url_params_route_status(client):
    response = client.get('/url_params')
    assert response.status_code == 200

def test_url_params_with_no_params(client):
    response = client.get('/url_params')
    assert b'No URL parameters provided' in response.data

def test_url_params_display_multiple_params(client):
    response = client.get('/url_params?name=Mahmud&group=231-352&test=value')
    assert b'name' in response.data
    assert b'Mahmud' in response.data
    assert b'group' in response.data
    assert b'231-352' in response.data
    assert b'test' in response.data
    assert b'value' in response.data