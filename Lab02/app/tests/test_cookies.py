def test_cookies_set_on_first_visit(client):
    response = client.get('/cookies')
    assert b'flask_lab_cookie' in response.data
    assert b'student_cookie' in response.data
    assert b'set' in response.data
    assert 'flask_lab_cookie=student_cookie' in response.headers.get('Set-Cookie', '')

def test_cookies_delete_on_second_visit(client):
    # First visit sets the cookie
    client.get('/cookies')
    
    # Second visit should delete it
    response = client.get('/cookies')
    assert b'delete' in response.data
    
    # Check cookie deletion headers
    set_cookie = response.headers.get('Set-Cookie', '')
    assert 'flask_lab_cookie=' in set_cookie  # Empty value
    assert 'expires=0' in set_cookie.lower() or 'max-age=0' in set_cookie.lower()
