def test_form_params_get_request(client):
    response = client.get('/form_params')
    assert response.status_code == 200
    assert b'Submit Form' in response.data
    assert b'No form data submitted yet' in response.data

def test_form_params_post_request(client):
    response = client.post('/form_params', data={
        'name': 'ali',
        'email': 'ali@mospoly.ru'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'ali' in response.data
    assert b'ali@mospoly.ru' in response.data
    assert b'Form submitted successfully' in response.data

def test_form_params_empty_submission(client):
    response = client.post('/form_params', data={}, follow_redirects=True)
    assert response.status_code == 200
    assert b'<table' not in response.data or b'No data available' in response.data