import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Database URL
SQLALCHEMY_DATABASE_URI = 'postgresql://bianca@localhost:5432/fyyur'

# Disable tracking modifications of objects and emit signals (default = None)
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_CHECK_DEFAULT = False
