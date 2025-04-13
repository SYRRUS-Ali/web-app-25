def test_phone_form_get_request(client):
    response = client.get('/phone_form')
    assert response.status_code == 200
    assert b'Phone Number Validation' in response.data
    assert b'Examples:' in response.data

def test_valid_phone_numbers(client):
    test_cases = [
        ('+7 (123) 456-75-90', '8-123-456-75-90'),
        ('8(123)4567590', '8-123-456-75-90'),
        ('123.456.75.90', '8-123-456-75-90'),
        ('+7 123 456 75 90', '8-123-456-75-90'),
        ('81234567590', '8-123-456-75-90')
    ]
    
    for phone, formatted in test_cases:
        response = client.post('/phone_form', data={'phone': phone})
        assert response.status_code == 200
        assert formatted.encode() in response.data
        assert b'Valid phone number!' in response.data

def test_invalid_phone_characters(client):
    invalid_cases = [
        '123#456$75',
        '8(123)45abc90',
        '123-456-75-9!',
        'phone-number'
    ]
    
    for phone in invalid_cases:
        response = client.post('/phone_form', data={'phone': phone})
        assert response.status_code == 200
        assert 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'.encode('utf-8') in response.data
        assert b'is-invalid' in response.data

def test_invalid_phone_length(client):
    invalid_cases = [
        ('123456789', '9 digits'),
        ('812345678901', '12 digits starting with 8'),
        ('12345678901', '11 digits not starting with 7 or 8')
    ]
    
    for phone, description in invalid_cases:
        response = client.post('/phone_form', data={'phone': phone})
        assert response.status_code == 200
        assert 'Недопустимый ввод. Неверное количество цифр.'.encode('utf-8') in response.data
        assert b'is-invalid' in response.data

def test_phone_form_preserves_input_on_error(client):
    test_phone = '123#456$75'
    response = client.post('/phone_form', data={'phone': test_phone})
    assert response.status_code == 200
    assert test_phone.encode() in response.data