from django.urls import path

from .json.dashboard_statistics import get_statistics
from .views import index

urlpatterns = [
    path('', index, name='index'),
]

