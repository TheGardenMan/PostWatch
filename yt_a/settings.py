import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_loc=BASE_DIR+'/templates'

MEDIA_URL = '/media/'#Don't care.Not to be used in production.Don't care.Will point to the below folder when serving media files.I don't think it's necessary.
MEDIA_ROOT = os.path.join(BASE_DIR, 'yt_site/raw_images')# Where to save uploaded files.
# print(MEDIA_ROOT)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&ytm6ivbvygw%q$3h*)3^poeej$na=qtn#s3)*7&!db%g6w+f='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['192.168.225.56','127.0.0.1','[2409:4072:629b:468:c479:a24:5ec1:2b13]']


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'yt_site',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	# removed the below because of csrf error in prod
	# https://stackoverflow.com/a/52947191/9217577
	# 'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yt_a.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		# Just tell where to look for html template files.Use "one forward slash only"..This DIRS have nothing to with project folder location.
		'DIRS': [template_loc],
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

WSGI_APPLICATION = 'yt_a.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'postgres',
		'USER': 'postgres',
		'PASSWORD': 'jaxtek',
		'HOST': 'localhost',
		'PORT': '5432',
	}
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# STATIC_URL = '/static/'  #required to serve static files ):
# STATIC_ROOT= [os.path.join(BASE_DIR, "static_files"),]
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static_files"),] #django look for static files here and app_name/static
