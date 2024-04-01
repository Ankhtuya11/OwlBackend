"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from datetime import datetime
from pathlib import Path
import json
import psycopg2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yz1pn$&wjvz!hq+bv!#odx(x%+9*3-lk(5&5n!un+2a9e4jdtj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '192.168.0.15',
    '127.0.0.1',
    '59.153.86.254'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backendApp',
    'rest_framework',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    # Add any other domains that should be allowed
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

def sendResponse(request,resultCode,data, action):
    resp = {}
    resp["resultCode"] = resultCode
    resp["resultMessage"] = resultMessages[resultCode]
    resp["data"] = data
    resp["size"] = len(data)
    resp["action"] = action
    resp["curdate"] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    return json.dumps(resp,indent=4, sort_keys=True, default=str)

#dbconnection
def connect():
    con = psycopg2.connect(
        dbname='qrOwl',
        user='userowl',
        password='Owl1234@',
        host='192.168.0.15',
        # host='59.153.86.254',
        port='5938',
    )
    return con
#connect --> function maani duusaj vnaaa ard iregdee
def disconnect(con):
    con.close()
#disconnect
    


def send_verification_email(email, verification_code,fname,lname):
    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = "pcniiacc@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Verification Code"

    # Email body
    body = f" <body><p style='font-family: sans-serif; font-size: 16px; line-height: 1.5; margin: 20px;'>Welcome {fname}, {lname}</p>Your verification code is: <a href='localhost:8000/checktoken/?token={verification_code}'>{verification_code}</body>"

    
    msg.attach(MIMEText(body, 'html'))

    # Send the message via SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "pcniiacc@gmail.com"
    smtp_password = "omlm sujr kczy gour"
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail("pcniiacc@gmail.com", email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)
   

resultMessages = {
    200:"Success",
    404:"Not found",
    1000 : "Burtgeh bolomjgui. Mail hayag umnu burtgeltei baina",
    1001 : "Hereglegch Amjilttai burtgegdlee. Batalgaajuulah mail ilgeegdlee. 24 tsagiin dotor batalgaajuulna.",
    1002 : "Batalgaajuulah mail ilgeelee",
    3001 : "ACTION BURUU",
    3002 : "METHOD BURUU",
    3003 : "JSON BURUU",
}   