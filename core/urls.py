from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.urls import re_path as url
from django.views.static import serve

from core.settings import BASE_DIR
from core.views import set_language

urlpatterns = [
    path('set-language/', set_language, name='set_language'),  # Tilni o'zgartirish
    path('admin/', admin.site.urls),
    path('user/', include('account.urls')),
    path('', include('exam.urls')),
    path('hemis/', include('authHemis.urls')),  # Hemis autentifikatsiya sahifasi
    path('main/', include('main.urls')),  # Hemis autentifikatsiya sahifasi
    path('log/', include('log.urls')),  # Hemis autentifikatsiya sahifasi
    path('edu/', include('university.urls')),  # Hemis autentifikatsiya sahifasi path('lib/', include('library.urls')),  # Hemis autentifikatsiya sahifasi

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

]

