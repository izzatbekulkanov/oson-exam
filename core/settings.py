import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

# .env faylni o'qish
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition
LOCAL_APPS = [
    'authHemis',
    'account',
    'university',
    'dashboard',
    'library',
    'api'
]
# Application definition

INSTALLED_OTHER_APPS = [
    'sass_processor',
    'widget_tweaks',
    'jazzmin',
    'rest_framework',
    'drf_yasg',
    'django_filters',
]

# Umumiy ilovalar (django.contrib va boshqa global ilovalar)
GLOBAL_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.utils.translation',
]

AUTH_USER_MODEL = 'account.CustomUser'

USER_AGENTS_CACHE = 'default'

AUTHENTICATION_BACKENDS = [
    'account.custom_backend.CustomBackend',
    'django.contrib.auth.backends.ModelBackend',
]

INSTALLED_APPS =INSTALLED_OTHER_APPS+ GLOBAL_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Lokalizatsiya middleware'i
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.permissions.IsAuthenticated',
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 200,
}

ROOT_URLCONF = 'core.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Yo'lni os.path.join() orqali yaratish
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

WSGI_APPLICATION = 'core.wsgi.application'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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

LANGUAGE_CODE = 'uz'
LANGUAGE_COOKIE_NAME = 'selected_language'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('uz', _("Uzbek")),
    ('en', _("English")),
    ('ru', _("Russian")),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    'DEEP_LINKING': True,
    'PERSIST_AUTHORIZATION': True,
    'DOC_EXPANSION': 'none',  # 'none', 'list' or 'full'
    'DEFAULT_MODEL_RENDERING': 'example',
    'SHOW_EXTENSIONS': True,
    'FILTER': True,
    'APIS_SORTER': 'alpha',
    'OPERATIONS_SORTER': 'alpha',
    'TAGS_SORTER': 'alpha',
    'DISPLAY_OPERATION_ID': True,
    'DEFAULT_MODEL_DEPTH': 2,
    'SHOW_REQUEST_HEADERS': True,
    'THEME': 'material',  # Alternatively you can use 'flattop' for a different look
}

swagger_ui_settings = {
    'deepLinking': True,
    'persistAuthorization': True,
    'defaultModelsExpandDepth': -1,
    'defaultModelExpandDepth': 5,
    'displayOperationId': False,
    'filter': True,
}

STATICFILES_FINDERS = [

    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/staticfiles/'  # String ko'rinishida bo'lishi kerak
MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR / 'staticfiles'  # Updated to 'staticfiles' to avoid confusion  # Ushbu o'zgaruvchi quti manbasiga qarab aniqlanadi
SASS_PROCESSOR_ROOT = BASE_DIR / 'staticfiles'  # Ushbu o'zgaruvchi quti manbasiga qarab aniqlanadi

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGOUT_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'

try:
    print("server ishlamadi va local ishladi")
    from core.local import *

except ImportError:
    print("local ishlamadi va server ishladi")
    from core.server import *

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Jazzmin Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Ulkanov",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Jazzmin",

    # Logo to use for your site, must be present in static files, used for brand on top left
    # "site_logo": "/assets/img/customizer/light.svg",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    # "login_logo": "/assets/img/customizer/light.svg",

    # Logo to use for login form in dark themes (defaults to login_logo)
    # "login_logo_dark": "/assets/customizer/light.svg",

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    # "site_icon": "/assets/img/customizer/light.svg",

    # Welcome text on the login screen
    "welcome_sign": "Assalomu aleykum Izzatbek Ulkanov Admin paneliga hush kelibsiz",

    # Copyright on the footer
    "copyright": "Izzatbek",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    # "search_model": ["authHemis.User", "authHemis.Group"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": "imageFile",

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["authHemis.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "authHemis.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "books"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    # "usermenu_links": [
    #     {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    #     {"model": "authHemis.user"}
    # ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (authHemis)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g authHemis.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["books", "books.author", "books.book"],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [{
            "name": "Make Messages",
            "url": "make_messages",
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    # for the full list of 5.13.0 free icon classes
    "icons": {
        "authHemis": "fas fa-users-cog",
        "authHemis.user": "fas fa-user",
        "authHemis.Group": "fas fa-users",
        "library.book": "fas fa-book",
        "account.customuser": "fas fa-user",  # CustomUser model
        "post.post": "fas fa-newspaper",  # Post model
        "university.group": "fas fa-users",  # Group model
    },

    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": True,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "vertical_tabs",
    # override change forms on a per modeladmin basis
    # "changeform_format_overrides": {"authHemis.user": "collapsible", "authHemis.group": "vertical_tabs"},
    # Add a language dropdown into the admin
}
