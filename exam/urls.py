from django.urls import path

from exam.landing_views import about_me, social, contact_me
from exam.views import employee_dashboard, dashboard, api_key

views_urlpatterns = [
    path('employee_dashboard', employee_dashboard, name='a_dashboard'),

    path('api_key', api_key, name='api_key'),

    path('', dashboard, name='dashboard'),
]
landing_views_urlpatterns = [
    path('about_me', about_me, name='about_me'),
    path('social', social, name='social'),
    path('contact_me', contact_me, name='contact_me'),
]


urlpatterns =views_urlpatterns + landing_views_urlpatterns