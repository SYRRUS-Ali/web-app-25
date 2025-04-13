def test_headers_route_status(client):
    response = client.get('/headers')
    assert response.status_code == 200

def test_headers_display_common_headers(client):
    response = client.get('/headers')
    assert b'Host' in response.data
    assert b'User-Agent' in response.data
    assert b'<table' in response.data
    assert b'Header' in response.data
    assert b'Value' in response.data

def test_custom_headers_display(client):
    custom_headers = {'X-Custom-Header': 'TestValue'}
    response = client.get('/headers', headers=custom_headers)
    assert b'X-Custom-Header' in response.data
    assert b'TestValue' in response.data