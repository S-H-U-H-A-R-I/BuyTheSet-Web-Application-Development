from pathlib import Path
DEBUG = True
SECRET_KEY = 'django-insecure-o-dzgrxhsrgh!30ypwb$1hh0dbiuq#n3sfzo1i+m8)0_i!uff6'
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
PAYSTACK_PUBLIC_KEY = '<API_KEY>'
PAYSTACK_SECRET_KEY = '<API_KEY>'
EMAIL_HOST_USER = '<EMAIL>'
EMAIL_HOST_PASSWORD = '<PASSWORD>'
MAPSJAVASCRIPT_API_KEY = '<API_KEY>'
DISTANCEMATRIX_API_KEY = '<API_KEY>'
