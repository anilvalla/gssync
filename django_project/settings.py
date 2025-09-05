import os
import dj_database_url
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Security and Performance
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-fallback-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Allowed Hosts
ALLOWED_HOSTS = [
    '.herokuapp.com',
    'localhost',
    '127.0.0.1',
    'web'  # Docker service name
]

# Use DATABASE_URL for Heroku
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# Additional Heroku-specific configurations
if 'DYNO' in os.environ:
    # Enable HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
