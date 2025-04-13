import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    # 1 hour
    REMEMBER_COOKIE_DURATION = 3600  