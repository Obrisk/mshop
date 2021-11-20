import os
import configparser
import requests

from .base import *


CAMEL_STORE_VERSION = '1.0.0'
SHOP_NAME = 'WineAndDine'         # 店铺名


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES
# ------------------------------------------------------------------------------
# http://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": env.db("DATABASE_URL"),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True


DEBUG = env.bool("DJANGO_DEBUG", False)


# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# ALB health check requests should be allowed, whitelist IP address 
def get_ec2_instance_ip():
    """
    Try to obtain the IP address of the current EC2 instance in AWS
    """
    try:
        ip = requests.get(
          'http://169.254.169.254/latest/meta-data/local-ipv4',
          timeout=5
        ).text
    except requests.exceptions.ConnectionError:
        logging.error('COULD NOT GET AWS EC2 INSTANCE IP')
        return None
    return ip


AWS_LOCAL_IP = get_ec2_instance_ip()

ALLOWED_HOSTS = [AWS_LOCAL_IP, 'www.wine-and-dine.cn', 'wine-and-dine.cn']

# DATABASES
# ------------------------------------------------------------------------------
DATABASES['default'] = env.db('DATABASE_URL')  # noqa F405
DATABASES['default']['ENGINE'] = 'django_db_geventpool.backends.postgresql_psycopg2'
DATABASES['default']['ATOMIC_REQUESTS'] = False  # From django-db-geventpool
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=0)  # From django-db-geventpool

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# This is not so important but added here to avoid confusion
# when generating CSRF token on Ajax requests
#https://docs.djangoproject.com/en/2.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie
#https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-CSRF_USE_SESSIONS
CSRF_USE_SESSIONS = True

# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 518400
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('SECURE_CONTENT_TYPE_NOSNIFF', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = 'DENY'


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env('SECRET_KEY')




AUTH_PASSWORD_VALIDATORS = []

INSTALLED_APPS += [
    'rest_framework.authtoken',
    'django_filters',
    'captcha',

    'qapi',
    'quser',
    'qcache',
    'qsmstoken',

    'apps.qfile',
    'wxapp',
    'apps.account',
    'apps.config',
    'apps.goods',
    'apps.group_buy',
    'apps.refund',
    'apps.trade',
    'apps.count',
    'apps.shop',
    'apps.user',
    'wx_pay',
    'apps.feedback',
    'apps.homepage',
    'apps.sms',
    'apps.tools',
    'apps.cloud',
    'apps.wx_logistics',
    'apps.short_video',
    'apps.utils',
]


# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '/var/tmp/django_cache',
        'TIMEOUT': 1 * 60 * 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        },
    },
    'qcache': {
        'BACKEND': 'qcache.no_pickle_cache_backend.NoPickleLocMemCache',
        'LOCATION': 'qcache-only',
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/api/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles/"),
]
MEDIA_URL = '/api/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#朋友圈分享海报
POSTER_ROOT = os.path.join(MEDIA_ROOT, 'poster')

if not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)

if not os.path.exists(POSTER_ROOT):
    os.mkdir(POSTER_ROOT)


CONFIG_FILE_PATH = os.path.join(BASE_DIR, "config.ini")
SETTINGS_CONFIG = configparser.ConfigParser()
SETTINGS_CONFIG.read(CONFIG_FILE_PATH)
SETTINGS_CONFIG_DEFAULT = SETTINGS_CONFIG["DEFAULT"]

if "WX_LITE_SECRET" in SETTINGS_CONFIG_DEFAULT:
    WX_LITE_SECRET = SETTINGS_CONFIG_DEFAULT["wx_lite_secret"]
else:
    WX_LITE_SECRET = os.environ.get('WX_LITE_SECRET')


AUTH_USER_MODEL = 'user.User'

SHOP_SITE = 'wine-and-dine'
NUMBER_OF_SHOP = 1    # 店铺数量

#七牛
QFILE_JUST_ALLOW_IMG = False
QFILE_QINIU_ACCESS_KEY = ''
QFILE_SECRET_KEY = ''
QFILE_QINIU_BUCKET_DOMAIN = ''
QFILE_QINIU_BUCKET_NAME = ''
QFILE_QINIU_SECURE_URL = False

# DEFAULT_FILE_STORAGE = 'apps.qfile.storage.qiniu.QiniuMediaStorage'
# STATICFILES_STORAGE = 'apps.qfile.storage.qiniu.QiniuStaticStorage'


#腾讯地图api KEY
TENCENT_LBS_KEY = ''
TENCENT_LBS_SK = ''


WX_CONFIG = {
    'WXAPP_APPID': '',
    'WXAPP_APPSECRET': '',
}


#微信支付相关
WX_PAY_APP_ID = ""  # 微信公众号 appid
WX_PAY_WXA_APP_ID = ""  # 小程序 appid
WX_PAY_API_KEY = ""  # 商户 key
WX_PAY_MCH_ID = ""  # 商户号
WX_PAY_SUB_MCH_ID = ""  # 子商户号，受理模式下必填
WX_PAY_MCH_CERT = os.path.join(BASE_DIR, "conf/cert_file/qichang/apiclient_cert.pem")  # 商户证书路径
WX_PAY_MCH_KEY = os.path.join(BASE_DIR, "conf/cert_file/qichang/apiclient_key.pem")  # 商户证书私钥路径
WX_PAY_NOTIFY_URL = "http://**.com/api/trade/"  # 支付结果通知回调
