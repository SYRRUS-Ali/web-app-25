from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите в систему'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

# User database with ali/ali2025
users = {
    'ali': {
        'password': generate_password_hash('ali2025'),
        'id': 'ali'
    },
    'mehrez': {
        'password': generate_password_hash('mehrez2025'),
        'id': 'mehrez'
    }
}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    if 'visits' not in session:
        session['visits'] = 0
    session['visits'] += 1
    return render_template('index.html', visits=session['visits'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember') == 'on'
        
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'])
            login_user(user_obj, remember=remember)
            flash('Вы успешно вошли в систему!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

if __name__ == '__main__':
    app.run(debug=True)