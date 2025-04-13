from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import re
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return redirect(url_for('url_params'))

@app.route('/url_params')
def url_params():
    return render_template('url_params.html')

@app.route('/headers')
def headers():
    return render_template('headers.html')

@app.route('/cookies')
def cookies():
    cookie_action = None
    cookie_value = None
    
    # Check if the cookie exists in the request
    if 'flask_lab_cookie' not in request.cookies:
        # Set the cookie in the response
        resp = make_response(render_template(
            'cookies.html',
            cookie_action='set',
            cookie_value='student_cookie'
        ))
        resp.set_cookie('flask_lab_cookie', 'student_cookie', max_age=60*60*24*7)
        return resp
    else:
        # Delete the cookie from the response
        resp = make_response(render_template(
            'cookies.html',
            cookie_action='delete'
        ))
        resp.delete_cookie('flask_lab_cookie')
        return resp

@app.route('/form_params', methods=['GET', 'POST'])
def form_params():
    form_data = None
    if request.method == 'POST':
        form_data = request.form
        flash('Form submitted successfully!', 'success')
    return render_template('form_params.html', form_data=form_data)

@app.route('/phone_form', methods=['GET', 'POST'])
def phone_form():
    error = None
    formatted_phone = None
    phone_input = request.form.get('phone', '') if request.method == 'POST' else None
    
    if request.method == 'POST':
        # Remove all non-digit characters for validation
        digits = re.sub(r'[^\d]', '', phone_input)
        
        # Check for invalid characters
        if not re.fullmatch(r'^[\d\s\(\)\-\.\+]+$', phone_input):
            error = "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
        # Check phone length
        elif (digits.startswith(('7', '8')) and len(digits) != 11) or \
             (not digits.startswith(('7', '8')) and len(digits) != 10):
            error = "Недопустимый ввод. Неверное количество цифр."
        else:
            # Format phone number to 8-***-***-**-**
            if digits.startswith('7'):
                digits = '8' + digits[1:]
            elif not digits.startswith('8') and len(digits) == 10:
                digits = '8' + digits
            
            formatted_phone = '-'.join([
                digits[0],
                digits[1:4],
                digits[4:7],
                digits[7:9],
                digits[9:]
            ])
    
    return render_template(
        'phone_form.html',
        error=error,
        formatted_phone=formatted_phone,
        phone_input=phone_input
    )


if __name__ == '__main__':
    app.run(debug=True)