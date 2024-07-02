from django.urls import path
from log.json.entry_loggin import entry_logging
from log.views import settings_log

views_urlpatterns = [
    path('entry_logging', entry_logging, name='entry_logging'),
    path('settings_log', settings_log, name='settings_log')
]
urlpatterns =views_urlpatterns