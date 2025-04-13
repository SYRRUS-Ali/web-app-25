import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-key-231-352'
    FLASK_ENV = os.getenv('FLASK_ENV') or 'development'